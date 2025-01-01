// Web app endpoint to serve the tracking pixel and track email opens
function doGet(e) {
  // Extract parameters from the GET request
  var firstName = e.parameter.first_name;
  var lastName = e.parameter.last_name;
  var email = e.parameter.email;
  var subject = e.parameter.subject;
  var body = e.parameter.body;

  // Generate a unique Tracking ID for this email
  var trackingId = generateTrackingId();

  // Send the email with the tracking ID
  var emailSent = sendEmail(email, subject, body, trackingId, firstName, lastName);

  // Log the result of email sending
  if (emailSent) {
    Logger.log("Email sent successfully to: " + email);
    logEmail(firstName, lastName, email, subject, true, trackingId);
  } else {
    Logger.log("Failed to send email to: " + email);
  }

  // Log the tracking request (this happens when the pixel is loaded)
  Logger.log("Tracking Pixel Loaded with ID: " + trackingId);

  logTrackingEvent(trackingId);

  // Return an empty response (1x1 pixel image)
  return ContentService.createTextOutput()
    .setMimeType(ContentService.MimeType.PNG)
    .setContent("1x1 pixel image here");
}

// Function to generate a unique tracking ID
function generateTrackingId() {
  return Utilities.getUuid();
}

// Function to send the email with tracking pixel
function sendEmail(recipient, subject, body, trackingId, firstName, lastName) {
  try {
    // Replace with your actual deployed Google Apps Script URL for the tracking pixel
    var trackingPixelUrl = "https://script.google.com/macros/s/AKfycbz7_yJx7GKiDcMWIxutR_bpPpsjwbGxHAZ4S-2wHP1m7pDUwwU5Ot5rl-cf1EVkLwTM/exec?trackingId=" + trackingId + "&email=" + recipient;

    // Create the HTML content, including the tracking pixel
    var bodyWithTracking = body + '<img src="' + trackingPixelUrl + '" width="0" height="0" style="display:none;" />';

    // Send the email with both plain text and HTML body
    MailApp.sendEmail({
      to: recipient,
      subject: subject,
      body: body,  // Plain text body for the email client
      htmlBody: bodyWithTracking  // HTML body to render the tracking pixel
    });

    return true;
  } catch (error) {
    Logger.log("Error sending email to " + recipient + ": " + error.message);
    return false;
  }
}

// Web app endpoint to trigger email sending and logging
function sendEmailWithTracking(firstName, lastName, email, subject, body) {
  // Generate a unique Tracking ID for this email
  var trackingId = generateTrackingId();

  // Send the email with the tracking ID
  var emailSent = sendEmail(email, subject, body, trackingId, firstName, lastName);

  // Log and return the result
  if (emailSent) {
    // Log the successful sending of the email
    Logger.log("Email sent successfully to: " + email);

    // Log the email details in the Google Sheet
    logEmail(firstName, lastName, email, subject, true, trackingId);

    return ContentService.createTextOutput("Email sent successfully!");
  } else {
    // Log the failure to send the email
    Logger.log("Failed to send email to: " + email);

    return ContentService.createTextOutput("Failed to send email.");
  }
}

// Function to log email details in a Google Sheet
function logEmail(firstName, lastName, email, subject, emailSent, trackingId) {
  try {
    var id = SpreadsheetApp.getActiveSpreadsheet().getId();
    var sheet = SpreadsheetApp.openById(id).getActiveSheet();

    // Log email details in the sheet
    var dateSent = new Date();
    sheet.appendRow([firstName, lastName, email, subject, dateSent, emailSent ? "Yes" : "No", trackingId, "No"]);

    Logger.log("Logged email details in sheet: " + firstName + " " + lastName + " " + trackingId);
  } catch (error) {
    Logger.log("Error logging email details: " + error.message);
  }
}