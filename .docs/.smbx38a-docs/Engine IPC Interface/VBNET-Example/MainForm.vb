Imports System.Collections.Generic
Imports System.Drawing
Imports System.Windows.Forms
Imports System.Runtime.InteropServices
Imports System.Collections

Friend Class ClassMemoryMapping
	<DllImport("Kernel32.dll", CharSet := CharSet.Auto)> _
	Private Shared Function OpenFileMapping(dwDesiredAccess As Integer, <MarshalAs(UnmanagedType.Bool)> bInheritHandle As Boolean, lpName As String) As IntPtr
	End Function
	<DllImport("Kernel32.dll", CharSet := CharSet.Auto)> _
	Private Shared Function MapViewOfFile(hFileMapping As IntPtr, dwDesiredAccess As UInteger, dwFileOffsetHigh As UInteger, dwFileOffsetLow As UInteger, dwNumberOfBytesToMap As UInteger) As IntPtr
	End Function
	<DllImport("Kernel32.dll", CharSet := CharSet.Auto)> _
	Private Shared Function UnmapViewOfFile(pvBaseAddress As IntPtr) As Boolean
	End Function
	<DllImport("Kernel32.dll", CharSet := CharSet.Auto)> _
	Private Shared Function CloseHandle(handle As IntPtr) As Boolean
	End Function
	Private Const FILE_MAP_ALL_ACCESS As Integer = &H2 Or &H4
	Private Const BUFFER_SIZE_INT As Integer = 8192
	Private Const SAFE_BUFFER_SIZE As Integer = 8000
	Private m_hSharedMemoryFile As IntPtr = IntPtr.Zero
	Private m_pwData As IntPtr = IntPtr.Zero
	Private m_bInit As Boolean = False
	Private ReadBuffer As Byte() = New Byte(8191) {}
	Private WriteBuffer As Byte() = New Byte(8191) {}
	Private SendArr As ArrayList = Nothing
	Private Messages As Queue(Of String) = Nothing
	Private ProcessTimer As System.Timers.Timer = Nothing
	Public Sub New()
		ProcessTimer = New System.Timers.Timer(15)
		ProcessTimer.Enabled = True
		ProcessTimer.AutoReset = True
		AddHandler ProcessTimer.Elapsed, New System.Timers.ElapsedEventHandler(AddressOf ProcessTimer_Elapsed)
		SendArr = New ArrayList()
		Messages = New Queue(Of String)()
	End Sub
	Protected Overrides Sub Finalize()
		Try
			If ProcessTimer IsNot Nothing Then
				ProcessTimer.Dispose()
				ProcessTimer = Nothing
			End If
			Close()
		Finally
			MyBase.Finalize()
		End Try
	End Sub
	Public ReadOnly Property initialized() As Boolean
		Get
			Return m_bInit
		End Get
	End Property
	Public ReadOnly Property HasMessage() As Boolean
		Get
			Return (Messages.Count > 0)
		End Get
	End Property
	Private Sub InitClient()
		If m_hSharedMemoryFile = IntPtr.Zero Then
			m_hSharedMemoryFile = OpenFileMapping(FILE_MAP_ALL_ACCESS, False, "smbx_memory_block")
		End If
		If m_hSharedMemoryFile <> IntPtr.Zero Then
			If m_pwData = IntPtr.Zero Then
				m_pwData = MapViewOfFile(m_hSharedMemoryFile, FILE_MAP_ALL_ACCESS, 0, 0, 0)
			End If
			If m_pwData <> IntPtr.Zero Then
				m_bInit = True
			End If
		End If
	End Sub
	Private Sub Close()
		If m_bInit Then
			UnmapViewOfFile(m_pwData)
			CloseHandle(m_hSharedMemoryFile)
		End If
	End Sub
	Private Sub Processing()
		If m_bInit Then
			Marshal.Copy(m_pwData, ReadBuffer, 0, BUFFER_SIZE_INT)
			Dim Msglen As Short = System.BitConverter.ToInt16(ReadBuffer, 0)
			If Msglen > 0 AndAlso Msglen < SAFE_BUFFER_SIZE Then
				Dim RevcText As String = System.Text.Encoding.ASCII.GetString(ReadBuffer, 2, Msglen)
				Dim CommandArr As String() = RevcText.Split(ControlChars.Lf)
				For i As Integer = 0 To CommandArr.Length - 1
					Messages.Enqueue(CommandArr(i))
				Next
				Array.Clear(ReadBuffer, 0, BUFFER_SIZE_INT)
				Marshal.Copy(ReadBuffer, 0, m_pwData, BUFFER_SIZE_INT)
			End If
			If SendArr.Count > 0 Then
				Marshal.Copy(New IntPtr(m_pwData.ToInt32() + BUFFER_SIZE_INT), WriteBuffer, 0, BUFFER_SIZE_INT)
				Dim BufLen As Short = System.BitConverter.ToInt16(WriteBuffer, 0)
				Dim DontClearArr As Boolean = (BufLen > 0 AndAlso BufLen < SAFE_BUFFER_SIZE)
				Dim SendBytes As Byte() = System.Text.Encoding.ASCII.GetBytes(String.Join(vbLf, DirectCast(SendArr.ToArray(GetType(String)), String())))
				BufLen = CShort(SendBytes.Length)
				Array.Clear(WriteBuffer, 0, BUFFER_SIZE_INT)
				If BufLen > 0 AndAlso BufLen < SAFE_BUFFER_SIZE Then
					Buffer.BlockCopy(System.BitConverter.GetBytes(BufLen), 0, WriteBuffer, 0, 2)
					Buffer.BlockCopy(SendBytes, 0, WriteBuffer, 2, BufLen)
				Else
					DontClearArr = False
				End If
				Marshal.Copy(WriteBuffer, 0, New IntPtr(m_pwData.ToInt32() + BUFFER_SIZE_INT), BUFFER_SIZE_INT)
				If DontClearArr = False Then
					SendArr.Clear()
				End If
			End If
		End If
	End Sub
	Public Sub SendMessageToMemoryBlock(CommandStr As String)
		If m_bInit Then
			SendArr.Add(CommandStr)
		End If
	End Sub
	Public Function GetMessageFromMemoryBlock(ByRef Message As String) As Boolean
		If m_bInit Then
			If Messages.Count > 0 Then
				Message = Messages.Dequeue()
				Return True
			End If
		End If
		Message = String.Empty
		Return False
	End Function
	Private Sub ProcessTimer_Elapsed(source As Object, e As System.Timers.ElapsedEventArgs)
		If m_bInit Then
			Processing()
		Else
			InitClient()
		End If
	End Sub
End Class
Public Partial Class MainForm
	Inherits Form
	Private CMM As ClassMemoryMapping = Nothing
	Private InitOK As Boolean = False
	Public Sub New()
		InitializeComponent()
	End Sub
	Private Sub Timer1Tick(sender As Object, e As EventArgs)
		If CMM Is Nothing Then
			CMM = New ClassMemoryMapping()
		Else
			If CMM.initialized = False Then
				button1.Enabled = False
				textBox1.Enabled = False
				textBox1.Text = "Please open smbx.exe with command line."
			Else
				If InitOK = False Then
					button1.Enabled = True
					textBox1.Enabled = True
					textBox1.Text = String.Empty
					InitOK = True
				End If
				If CMM.HasMessage Then
					Dim Message As String = Nothing
					While CMM.GetMessageFromMemoryBlock(Message)
						listBox1.Items.Add(Message)
					End While
				End If
			End If
		End If
	End Sub
	Private Sub Button1Click(sender As Object, e As EventArgs)
		Dim Message As String = textBox1.Text
		If Message.Length > 0 Then
			listBox2.Items.Add(Message)
			CMM.SendMessageToMemoryBlock(Message)
			textBox1.Text = String.Empty
		End If
	End Sub
End Class
