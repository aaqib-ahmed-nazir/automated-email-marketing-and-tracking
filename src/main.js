function doGet(e) {
  var firstName = e.parameter.first_name;
  var lastName = e.parameter.last_name;
  var email = e.parameter.email;
  var subject = e.parameter.subject;
  var body = e.parameter.body;

  var trackingId = generateTrackingId();

  var emailSent = sendEmail(email, subject, body, trackingId, firstName, lastName);

  if (emailSent) {
    Logger.log("Email sent successfully to: " + email);
    logEmail(firstName, lastName, email, subject, true, trackingId);
  } else {
    Logger.log("Failed to send email to: " + email);
  }

  Logger.log("Tracking Pixel Loaded with ID: " + trackingId);

  logTrackingEvent(trackingId);

  return ContentService.createTextOutput()
    .setMimeType(ContentService.MimeType.PNG)
    .setContent("1x1 pixel image here");
}

function generateTrackingId() {
  return Utilities.getUuid();
}

function sendEmail(recipient, subject, body, trackingId, firstName, lastName) {
  try {
    var trackingPixelUrl = "https://script.google.com/macros/s/AKfycbz7_yJx7GKiDcMWIxutR_bpPpsjwbGxHAZ4S-2wHP1m7pDUwwU5Ot5rl-cf1EVkLwTM/exec?trackingId=" + trackingId + "&email=" + recipient;

    var bodyWithTracking = body + '<img src="' + trackingPixelUrl + '" width="0" height="0" style="display:none;" />';

    MailApp.sendEmail({
      to: recipient,
      subject: subject,
      body: body,
      htmlBody: bodyWithTracking
    });

    return true;
  } catch (error) {
    Logger.log("Error sending email to " + recipient + ": " + error.message);
    return false;
  }
}

function sendEmailWithTracking(firstName, lastName, email, subject, body) {
  var trackingId = generateTrackingId();

  var emailSent = sendEmail(email, subject, body, trackingId, firstName, lastName);

  if (emailSent) {
    Logger.log("Email sent successfully to: " + email);

    logEmail(firstName, lastName, email, subject, true, trackingId);

    return ContentService.createTextOutput("Email sent successfully!");
  } else {
    Logger.log("Failed to send email to: " + email);

    return ContentService.createTextOutput("Failed to send email.");
  }
}

function logEmail(firstName, lastName, email, subject, emailSent, trackingId) {
  try {
    var id = SpreadsheetApp.getActiveSpreadsheet().getId();
    var sheet = SpreadsheetApp.openById(id).getActiveSheet();

    var dateSent = new Date();
    sheet.appendRow([firstName, lastName, email, subject, dateSent, emailSent ? "Yes" : "No", trackingId, "No"]);

    Logger.log("Logged email details in sheet: " + firstName + " " + lastName + " " + trackingId);
  } catch (error) {
    Logger.log("Error logging email details: " + error.message);
  }
}