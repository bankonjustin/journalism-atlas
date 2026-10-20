/**
 * SmartNews x Atlas intake: Google Apps Script web app that appends each form submission to a Google Sheet.
 * Receives the POST from preview/smartnews-d029dc36/index.html (later partners/smartnews.html), page_version smartnews-page-v1.0.
 *
 * DEPLOY STEPS (Justin, about five minutes)
 *   1. Create a Google Sheet named "SmartNews intake" and share it with Ryan (edit or view).
 *   2. In the Sheet: Extensions > Apps Script. Delete the starter code and paste this whole file. Save.
 *   3. (Optional) Set SHEET_NAME below. The script creates the tab and header row on the first submission.
 *   4. Deploy > New deployment > type "Web app".
 *        Execute as:      Me
 *        Who has access:  Anyone          (the page posts without sign-in; this is required)
 *      Click Deploy and approve the permission prompt. Copy the Web app URL (ends in /exec).
 *   5. In the page, paste the URL into the single constant:   const FORM_ENDPOINT = "https://script.google.com/macros/s/.../exec";
 *   6. Test: open the page, submit a test application, confirm a row appears. Delete the test row.
 *   7. After any later edit to this script: Deploy > Manage deployments > Edit > Version: New version. The URL stays the same.
 *
 * NOTES
 *   - The page sends with mode "no-cors", so the browser cannot read the response. A script error would look like success
 *     to the applicant. Check the Sheet (and Apps Script > Executions) after the first few submissions.
 *   - The honeypot field (company_website) is checked in the page. It is checked here too as a second layer.
 *   - Column names map to the Atlas pipeline: link_primary -> Link Primary; platform_primary -> Platform Primary
 *     (controlled vocab, or "Other"); group -> Groups (controlled vocab, or "Other"); location -> Geography (free text).
 *     frequency feeds the Rule 7 inactivity check at intake.
 */

var SHEET_NAME = 'Applications';

var COLUMNS = [
  'submitted_at',        // ISO timestamp, set by the page
  'source',              // always "smartnews-page"
  'page_version',        // e.g. "smartnews-page-v1.0"
  'mode',                // "self" or "recommend"
  'interested_in',       // election-pilot; future-phases; other-opportunities (semicolon-separated)
  'name',                // applicant, or the person being recommended
  'email',               // applicant's email (may be empty in recommend mode)
  'recommender_name',    // recommend mode only
  'recommender_email',   // recommend mode only
  'publication',
  'link_primary',        // Link Primary
  'platform_primary',    // Platform Primary vocab value, or "Other"
  'group',               // Groups vocab value, or "Other"
  'location',            // free text; maps loosely to Geo fields
  'frequency',           // weekly-plus | few-per-month | monthly | less | ""
  'notes',
  'consent',             // "yes"
  'received_at'          // server time, for audit
];

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var p = (e && e.parameter) || {};
    if (p.company_website) return respond_({ ok: true });   // honeypot tripped: ignore silently

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(COLUMNS);
      sheet.setFrozenRows(1);
    }

    var row = COLUMNS.map(function (c) {
      if (c === 'received_at') return new Date();
      return clean_(p[c]);
    });
    sheet.appendRow(row);
    return respond_({ ok: true });
  } catch (err) {
    return respond_({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

// Visiting the URL in a browser confirms the deployment is live (it does not write anything).
function doGet() {
  return respond_({ ok: true, service: 'smartnews-intake', page_version_expected: 'smartnews-page-v1.0' });
}

// Neutralise spreadsheet formula injection: a leading = + - @ would be evaluated as a formula.
function clean_(v) {
  var s = (v == null ? '' : String(v)).trim().slice(0, 2000);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

function respond_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
