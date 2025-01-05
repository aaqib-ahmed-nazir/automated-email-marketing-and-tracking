function sendEmails() {
  /*
      - Parameters:
          - None 

      - Return: 
          - None

      - Description:
          - Send emails to the recipients in the Google Sheet.
          - Rotate through the aliases to send emails.
          - Update the status of the email in the Google Sheet.
  */
  var id = SpreadsheetApp.getActiveSpreadsheet().getId();
  var sheet = SpreadsheetApp.openById(id).getActiveSheet();
  var data = sheet.getDataRange().getValues();

  var aliases = GmailApp.getAliases(); 
  if (aliases.length === 0) {
    Logger.log("No aliases available.");
    return;
  }

  var aliasCount = aliases.length;

  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    var email = row[0];
    var subject = row[1];
    var emailContent = row[2];
    var openTrackingCell = sheet.getRange(i + 1, 5); // Open Email Tracking
    var lastSentCell = sheet.getRange(i + 1, 4);     // Last Sent
    var openAmountCell = sheet.getRange(i + 1, 7);   // Open Amount Column
    var sentTimestampCell = sheet.getRange(i + 1, 8); // Sent Timestamp Column

    // Rotate through aliases
    var aliasToUse = aliases[i % aliasCount];

    var trackingPixelUrl = "https://script.google.com/macros/s/AKfycbzdO2x6sX_gdQ2bEkIDlKQzdX9Z4LvNbLg-qCZsT_pG1GIyj7oht3Ow0LYIlcw-TJZL/exec?email=" + encodeURIComponent(email);

    var emailBody = emailContent + 
      `<br><img class="ajT" src="${trackingPixelUrl}" width="1" height="1" style="display:none;">`;

    if (MailApp.getRemainingDailyQuota() > 0) {
      try {
        GmailApp.sendEmail(email, subject, '', {
          htmlBody: emailBody,
          from: aliasToUse,  
          name: 'Arc Browser inc.'
        });

        // Set the initial status as "Sent"
        openTrackingCell.setValue("Sent");
        lastSentCell.setValue(new Date());
        
        // Set the sent timestamp
        sentTimestampCell.setValue(new Date());

        openAmountCell.setValue(""); 

        Logger.log("Email sent successfully to: " + email + " from: " + aliasToUse);
      } catch (error) {
        Logger.log("Error sending email to " + email + ": " + error.message);
        openTrackingCell.setValue("Failed");
      }
    } else {
      Logger.log("Daily quota exceeded.");
      break;
    }
  }
}

function doGet(e) {
  /*
      - Parameters:
          - e: Object containing the GET request parameters.

      - Return:
          - ContentService: Tracking pixel image.

      - Description:
          - Handle the GET request to the tracking pixel URL.
          - Update the email status to "Opened" in the Google Sheet.
  */
  if (!e || !e.parameter || !e.parameter.email) {
    Logger.log("No parameters found in GET request.");
    return ContentService.createTextOutput("Error: Missing parameters.");
  }

  var emailToTrack = e.parameter.email;

  var userAgent = e.parameter['User-Agent'] || 'Unknown';
  var referer = e.parameter['Referer'] || 'Unknown';

  Logger.log('Request received for email: ' + emailToTrack + ', User-Agent: ' + userAgent + ', Referer: ' + referer);

  var id = SpreadsheetApp.getActiveSpreadsheet().getId();
  var sheet = SpreadsheetApp.openById(id).getActiveSheet();
  var data = sheet.getDataRange().getValues();

  var emailIndex = 0;
  var sentTimestampIndex = 7; 
  var openTrackingIndex = 4;
  var openAmountIndex = 6;
  var lastOpenIndex = 5;

  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    var email = row[emailIndex];

    if (email === emailToTrack) {
      var sentTimestamp = row[sentTimestampIndex];
      
      if (sentTimestamp) {
        var now = new Date();
        var diff = (now - sentTimestamp) / 1000; 

        if (diff < 10) {
          Logger.log("Skipping first request for email: " + emailToTrack);
          return ContentService.createTextOutput("");  
        }

        updateEmailStatus(emailToTrack);
        break;
      }
    }
  }

  var pixel = Utilities.newBlob("", "image/gif").getBytes();
  return ContentService.createTextOutput(pixel).setMimeType(ContentService.MimeType.GIF);
}

function updateEmailStatus(emailToTrack) {
  /*
      - Parameters:
          - emailToTrack: Email address to track.

      - Return:
          - None

      - Description:  
          - Update the email status to "Opened" in the Google Sheet.
          - Update the open count and last open timestamp.
  */
  var id = SpreadsheetApp.getActiveSpreadsheet().getId();
  var sheet = SpreadsheetApp.openById(id).getActiveSheet();
  var data = sheet.getDataRange().getValues();

  var headers = data[0];
  var emailIndex = 0;
  var openTrackingIndex = 4;
  var lastSentIndex = 3;
  var openAmountIndex = 6;
  var lastOpenIndex = 5;

  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    var email = row[emailIndex];

    if (email === emailToTrack) {
      var currentOpenCount = row[openAmountIndex] || 0;
      var newOpenCount = currentOpenCount + 1;

      sheet.getRange(i + 1, openTrackingIndex + 1).setValue("Opened");
      sheet.getRange(i + 1, openAmountIndex + 1).setValue(newOpenCount);

      var formattedDate = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd HH:mm:ss");
      sheet.getRange(i + 1, lastOpenIndex + 1).setValue(formattedDate);

      Logger.log("Updated email status and open count for: " + emailToTrack);
      break;
    }
  }
}