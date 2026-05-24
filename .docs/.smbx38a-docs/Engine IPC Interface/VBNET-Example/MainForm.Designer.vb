Partial Class MainForm
	Private components As System.ComponentModel.IContainer = Nothing
	Protected Overrides Sub Dispose(disposing As Boolean)
		If disposing Then
			If components IsNot Nothing Then
				components.Dispose()
			End If
		End If
		MyBase.Dispose(disposing)
	End Sub
	Private Sub InitializeComponent()
		Me.components = New System.ComponentModel.Container()
		Me.listBox1 = New System.Windows.Forms.ListBox()
		Me.listBox2 = New System.Windows.Forms.ListBox()
		Me.textBox1 = New System.Windows.Forms.TextBox()
		Me.button1 = New System.Windows.Forms.Button()
		Me.timer1 = New System.Windows.Forms.Timer(Me.components)
		Me.SuspendLayout
		Me.listBox1.FormattingEnabled = true
		Me.listBox1.ItemHeight = 15
		Me.listBox1.Location = New System.Drawing.Point(12, 12)
		Me.listBox1.Name = "listBox1"
		Me.listBox1.Size = New System.Drawing.Size(296, 334)
		Me.listBox1.TabIndex = 0
		Me.listBox2.FormattingEnabled = true
		Me.listBox2.ItemHeight = 15
		Me.listBox2.Location = New System.Drawing.Point(323, 12)
		Me.listBox2.Name = "listBox2"
		Me.listBox2.Size = New System.Drawing.Size(306, 334)
		Me.listBox2.TabIndex = 1
		Me.textBox1.Location = New System.Drawing.Point(14, 362)
		Me.textBox1.Name = "textBox1"
		Me.textBox1.Size = New System.Drawing.Size(515, 25)
		Me.textBox1.TabIndex = 2
		Me.button1.Location = New System.Drawing.Point(535, 362)
		Me.button1.Name = "button1"
		Me.button1.Size = New System.Drawing.Size(94, 25)
		Me.button1.TabIndex = 3
		Me.button1.Text = "Send"
		Me.button1.UseVisualStyleBackColor = true
		AddHandler Me.button1.Click, AddressOf Me.Button1Click
		Me.timer1.Enabled = true
		Me.timer1.Interval = 15
		AddHandler Me.timer1.Tick, AddressOf Me.Timer1Tick
		Me.AutoScaleDimensions = New System.Drawing.SizeF(8!, 15!)
		Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
		Me.ClientSize = New System.Drawing.Size(639, 397)
		Me.Controls.Add(Me.button1)
		Me.Controls.Add(Me.textBox1)
		Me.Controls.Add(Me.listBox2)
		Me.Controls.Add(Me.listBox1)
		Me.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle
		Me.MaximizeBox = false
		Me.Name = "MainForm"
		Me.Text = "VB.NET-Example"
		Me.ResumeLayout(false)
		Me.PerformLayout
	End Sub
	Private timer1 As System.Windows.Forms.Timer
	Private button1 As System.Windows.Forms.Button
	Private textBox1 As System.Windows.Forms.TextBox
	Private listBox2 As System.Windows.Forms.ListBox
	Private listBox1 As System.Windows.Forms.ListBox
End Class
