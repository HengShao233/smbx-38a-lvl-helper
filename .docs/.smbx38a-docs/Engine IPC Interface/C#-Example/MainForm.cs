using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;
using System.Runtime.InteropServices;
using System.Collections;

namespace C__Example
{
    internal class ClassMemoryMapping
    {
        [DllImport("Kernel32.dll", CharSet = CharSet.Auto)]
        private static extern IntPtr OpenFileMapping(int dwDesiredAccess,[MarshalAs(UnmanagedType.Bool)] bool bInheritHandle,string lpName);
        [DllImport("Kernel32.dll", CharSet = CharSet.Auto)]
        private static extern IntPtr MapViewOfFile(IntPtr hFileMapping,uint dwDesiredAccess, uint dwFileOffsetHigh, uint dwFileOffsetLow,uint dwNumberOfBytesToMap);
        [DllImport("Kernel32.dll", CharSet = CharSet.Auto)]
        private static extern bool UnmapViewOfFile(IntPtr pvBaseAddress);
        [DllImport("Kernel32.dll", CharSet = CharSet.Auto)]
        private static extern bool CloseHandle(IntPtr handle);
        private const int FILE_MAP_ALL_ACCESS = 0x0002 | 0x0004;
        private const int BUFFER_SIZE_INT = 8192;
        private const int SAFE_BUFFER_SIZE = 8000;
        private IntPtr m_hSharedMemoryFile = IntPtr.Zero;
        private IntPtr m_pwData = IntPtr.Zero;
        private bool m_bInit = false;
        private byte[] ReadBuffer = new byte[8192];
        private byte[] WriteBuffer = new byte[8192];
        private ArrayList SendArr = null;
        private Queue<string> Messages = null;
        private System.Timers.Timer ProcessTimer = null;
        public ClassMemoryMapping()  {
			ProcessTimer = new System.Timers.Timer(15);
			ProcessTimer.Enabled = true;
			ProcessTimer.AutoReset = true;
			ProcessTimer.Elapsed += new System.Timers.ElapsedEventHandler(ProcessTimer_Elapsed);
			SendArr = new ArrayList();
			Messages = new Queue<string>();
        }
        ~ClassMemoryMapping() {
			if (ProcessTimer != null) {
				ProcessTimer.Dispose();
				ProcessTimer = null;
			}
			Close();
        }
        public bool initialized {
        	get {return m_bInit;}
        }
        public bool HasMessage {
        	get {return (Messages.Count > 0);}
        }
		private void InitClient() {
        	if (m_hSharedMemoryFile == IntPtr.Zero) {
        		m_hSharedMemoryFile = OpenFileMapping(FILE_MAP_ALL_ACCESS, false, "smbx_memory_block");
        	}
			if (m_hSharedMemoryFile != IntPtr.Zero) {
        		if (m_pwData == IntPtr.Zero) {
        			m_pwData = MapViewOfFile(m_hSharedMemoryFile, FILE_MAP_ALL_ACCESS, 0, 0, 0);
        		}
        		if (m_pwData != IntPtr.Zero) {
        			m_bInit = true;
        		}
			}
		}
		private void Close() {
			if (m_bInit) {
				UnmapViewOfFile(m_pwData);
				CloseHandle(m_hSharedMemoryFile);
			}
		}
        private void Processing() {
        	if (m_bInit) {
        		Marshal.Copy(m_pwData, ReadBuffer, 0, BUFFER_SIZE_INT);
        		short Msglen = System.BitConverter.ToInt16(ReadBuffer, 0);
        		if (Msglen > 0 && Msglen < SAFE_BUFFER_SIZE) {
        			string RevcText = System.Text.Encoding.ASCII.GetString(ReadBuffer, sizeof(short), Msglen);
        			string[] CommandArr = RevcText.Split('\n');
        			for (int i = 0; i < CommandArr.Length; i++) {
        				Messages.Enqueue(CommandArr[i]);
        			}
	        		Array.Clear(ReadBuffer, 0, BUFFER_SIZE_INT);
	        		Marshal.Copy(ReadBuffer, 0, m_pwData, BUFFER_SIZE_INT);					
        		}
        		if (SendArr.Count > 0) {
        			Marshal.Copy(new IntPtr(m_pwData.ToInt32() + BUFFER_SIZE_INT), WriteBuffer, 0, BUFFER_SIZE_INT);
        			short BufLen = System.BitConverter.ToInt16(WriteBuffer, 0);
        			bool DontClearArr = (BufLen > 0 && BufLen < SAFE_BUFFER_SIZE);
        			byte[] SendBytes = System.Text.Encoding.ASCII.GetBytes(string.Join("\n", (string[])SendArr.ToArray(typeof(string))));
        			BufLen = (short)SendBytes.Length;
        			Array.Clear(WriteBuffer, 0, BUFFER_SIZE_INT);
        			if (BufLen > 0 && BufLen < SAFE_BUFFER_SIZE) {
        				Buffer.BlockCopy(System.BitConverter.GetBytes(BufLen), 0, WriteBuffer, 0, sizeof(short));
        				Buffer.BlockCopy(SendBytes, 0, WriteBuffer, sizeof(short), BufLen);
        			}else {
        				DontClearArr = false;
        			}
        			Marshal.Copy(WriteBuffer, 0, new IntPtr(m_pwData.ToInt32() + BUFFER_SIZE_INT), BUFFER_SIZE_INT);
        			if (DontClearArr == false) SendArr.Clear();
        		}
        	}
        }
        public void SendMessageToMemoryBlock(string CommandStr) {
        	if (m_bInit) {
        		SendArr.Add(CommandStr);
        	}
        }
        public bool GetMessageFromMemoryBlock(out string Message) {
        	if (m_bInit) {
        		if (Messages.Count > 0) {
        			Message = Messages.Dequeue();
        			return true;
        		}
        	}
        	Message = string.Empty;
        	return false;
        }
        private void ProcessTimer_Elapsed(object source, System.Timers.ElapsedEventArgs e) {
        	if (m_bInit) {
        		Processing();
        	}else {
        		InitClient();
        	}
        }
    }
	public partial class MainForm : Form
	{
		private ClassMemoryMapping CMM = null;
		private bool InitOK = false;
		public MainForm()
		{
			InitializeComponent();
		}
		void Timer1Tick(object sender, EventArgs e)
		{
			if (CMM == null) {
				CMM = new ClassMemoryMapping();
			}else {
				if (CMM.initialized == false) {
					button1.Enabled = false;
					textBox1.Enabled = false;
					textBox1.Text = "Please open smbx.exe with command line.";
				}else {
					if (InitOK == false) {
						button1.Enabled = true;
						textBox1.Enabled = true;
						textBox1.Text = string.Empty;
						InitOK = true;
					}
					if (CMM.HasMessage) {
						string Message = null;
						while (CMM.GetMessageFromMemoryBlock(out Message)) {
							listBox1.Items.Add(Message);
						}
					}
				}
			}
		}
		void Button1Click(object sender, EventArgs e)
		{
			string Message = textBox1.Text;
			if (Message.Length > 0) {
				listBox2.Items.Add(Message);
				CMM.SendMessageToMemoryBlock(Message);
				textBox1.Text = string.Empty;				
			}
		}
	}
}
