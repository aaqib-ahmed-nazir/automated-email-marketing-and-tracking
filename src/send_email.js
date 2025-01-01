function doPost(e) {
  try {
    var firstName = e.parameter.first_name;
    var lastName = e.parameter.last_name;
    var email = e.parameter.email;
    var subject = e.parameter.subject;
    var body = e.parameter.body;

    MailApp.sendEmail({
      to: email,
      subject: subject,
      body: body,
      htmlBody: body
    });

    return ContentService.createTextOutput("Success")
        .setMimeType(ContentService.MimeType.TEXT);
  } catch (error) {
    return ContentService.createTextOutput("Error: " + error.message)
        .setMimeType(ContentService.MimeType.TEXT);
  }
}