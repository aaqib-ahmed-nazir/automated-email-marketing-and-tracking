function sendEmail(recipient, subject, body, trackingId) {
  try {
    var trackingPixelUrl = "https://script.google.com/macros/s/AKfycbz7_yJx7GKiDcMWIxutR_bpPpsjwbGxHAZ4S-2wHP1m7pDUwwU5Ot5rl-cf1EVkLwTM/exec?trackingId=" + trackingId;

    var bodyWithTracking = body + '<img src="' + trackingPixelUrl + '" width="1" height="1" style="display:none;" />';

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

function logEmail(firstName, lastName, email, subject, emailSent, trackingId) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    var dateSent = new Date();
    sheet.appendRow([firstName, lastName, email, subject, dateSent, emailSent ? "Yes" : "No", trackingId, "No"]);

    Logger.log("Logged email details in sheet: " + firstName + " " + lastName + " " + trackingId);
  } catch (error) {
    Logger.log("Error logging email details: " + error.message);
  }
}

function sendEmailWithTracking(firstName, lastName, email, subject, body) {
  var trackingId = Utilities.getUuid();

  var emailSent = sendEmail(email, subject, body, trackingId);

  if (emailSent) {
    logEmail(firstName, lastName, email, subject, true, trackingId);
    return ContentService.createTextOutput("Email sent successfully!");
  } else {
    return ContentService.createTextOutput("Failed to send email.");
  }
}

function doPost(e) {
  try {
    var params = JSON.parse(e.postData.contents);

    var firstName = params.first_name;
    var lastName = params.last_name;
    var email = params.email;
    var subject = params.subject;
    var body = params.body;

    return sendEmailWithTracking(firstName, lastName, email, subject, body);
  } catch (error) {
    Logger.log("Error in doPost: " + error.message);
    return ContentService.createTextOutput("Error: " + error.message).setMimeType(ContentService.MimeType.TEXT);
  }
}

function doGet(e) {
  var trackingId = e.parameter.trackingId;
  Logger.log("Tracking Pixel Loaded with ID: " + trackingId);

  return ContentService.createTextOutput("1x1 pixel image here").setMimeType(ContentService.MimeType.PNG);
}