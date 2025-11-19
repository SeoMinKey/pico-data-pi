function doPost(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  try {
    const data = JSON.parse(e.postData.contents);

    sheet.appendRow([
      new Date(),
      data.temperature,
      data.humidity,
      data.device
    ]);

    return ContentService.createTextOutput("OK")
        .setMimeType(ContentService.MimeType.TEXT);

  } catch (error) {
    return ContentService.createTextOutput("ERROR: " + error)
        .setMimeType(ContentService.MimeType.TEXT);
  }
}
