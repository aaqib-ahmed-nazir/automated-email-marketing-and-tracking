function sendEmails() {
  /*
      - Parameters:
        - None
      
      - Returns: 
        - None
      
      - Description:
        - This function sends emails to the recipients listed in the Google Sheet.
  */

  var id = SpreadsheetApp.getActiveSpreadsheet().getId();
  var sheet = SpreadsheetApp.openById(id).getActiveSheet();
  var data = sheet.getDataRange().getValues();

  for (var i = 1; i <= 2 && i < data.length; i++) {
    var row = data[i];
    var email = row[0];
    var subject = row[1];
    var emailContent = row[2];
    var openTrackingCell = sheet.getRange(i + 1, 5);
    var lastSentCell = sheet.getRange(i + 1, 4);
    var openAmountCell = sheet.getRange(i + 1, 7);

    var trackingPixelUrl = "https://script.google.com/macros/s/AKfycbzdO2x6sX_gdQ2bEkIDlKQzdX9Z4LvNbLg-qCZsT_pG1GIyj7oht3Ow0LYIlcw-TJZL/exec?email=" + encodeURIComponent(email);

    var emailBody = emailContent + 
      `<br><img class="ajT" src="${trackingPixelUrl}" width="1" height="1" style="display:none;">`;

    if (MailApp.getRemainingDailyQuota() > 0) {
      try {
        GmailApp.sendEmail(email, subject, '', {
          htmlBody: emailBody,
          name: 'Your Company Name'
        });

        openTrackingCell.setValue("Sent");
        lastSentCell.setValue(new Date());
        Logger.log("Email sent successfully to: " + email);
      } catch (error) {
        Logger.log("Error sending email to " + email + ": " + error.message);
        openTrackingCell.setValue("Failed");
      }
    } else {
      Logger.log("Daily email quota exceeded. Cannot send emails.");
      break;
    }
  }
}

function doGet(e) {
   /*
      - Parameters:
        - e: Object containing the GET request parameters.
      
      - Returns: 
        - ContentService: Text output with MIME type set to GIF.
      
      - Description:
        - This function is called when the tracking pixel URL is accessed.
          It updates the email status and open count in the Google Sheet
  */  

  if (!e || !e.parameter || !e.parameter.email) {
    Logger.log("No parameters found in GET request.");
    return ContentService.createTextOutput("Error: Missing parameters.");
  }

  var emailToTrack = e.parameter.email;
  
  var userAgent = e.parameter['User-Agent'] || 'Unknown';
  var referer = e.parameter['Referer'] || 'Unknown';

  Logger.log('Request received for email: ' + emailToTrack + ', User-Agent: ' + userAgent + ', Referer: ' + referer);

  updateEmailStatus(emailToTrack);

  var pixel = Utilities.newBlob("", "image/gif").getBytes();
  return ContentService.createTextOutput(pixel).setMimeType(ContentService.MimeType.GIF);
}

function updateEmailStatus(emailToTrack) {
  /*
      - Parameters:
        - emailToTrack: Email address to track.
      
      - Returns: 
        - None
      
      - Description:
        - This function updates the email status and open count in the Google Sheet
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