# Google Form Setup Guide for Photo Collection

This guide will help you set up the Google Form to collect creator photos and contact information.

## Step 1: Create the Google Form

1. Go to [Google Forms](https://forms.google.com)
2. Click **+ Blank** to create a new form
3. Name your form: "Atlas Creator Photo Collection"
4. Add a description (optional): "Photos submitted by creators for their Atlas profiles"

## Step 2: Add Form Fields

Add the following fields to your form **in this exact order**:

### Field 1: Creator Name
- **Type**: Short answer
- **Question**: "Your Name"
- **Description**: "What name should we use to identify you?"
- **Required**: No (make it optional)

### Field 2: Email Address
- **Type**: Short answer (or use Email type for validation)
- **Question**: "Email Address"
- **Description**: "We'll only contact you about using your photo"
- **Required**: No (make it optional)
- **Validation** (optional): Response validation → Email → Is valid email

### Field 3: Photo Upload
- **Type**: File upload
- **Question**: "Your Photo"
- **Description**: "Upload a square photo (500x500px or larger recommended)"
- **Required**: No (make it optional)
- **File upload settings**:
  - Allow only specific file types: Images (JPG, PNG)
  - Maximum file size: 10 MB (or adjust as needed)
  - Maximum number of files: 1

**Important:** You'll need to enable file uploads in Google Forms:
- When you add the File upload question, Google will prompt you to sign in
- File uploads require respondents to sign in to their Google account
- Files will be stored in a folder in your Google Drive

### Field 4: Timestamp
Google Forms automatically captures submission timestamp - no need to add this manually.

## Step 3: Configure Form Settings

1. Click the ⚙️ **Settings** icon at the top
2. Under **Responses**:
   - ✅ Check "Collect email addresses" (optional, but recommended)
   - ✅ Check "Limit to 1 response" if you want to prevent duplicate submissions
3. Under **Presentation**:
   - ✅ Check "Show progress bar" (optional)
   - Set confirmation message: "Thank you! We received your photo and will be in touch if we'd like to use it in your Atlas profile."

## Step 4: Get Form Entry IDs

To connect the form to the creator portal, you need to find the "entry IDs" for each field:

### Method 1: Inspect Form (Recommended)
1. Click the **Preview** button (eye icon) to open the form
2. Right-click on the page → **Inspect** (or press F12)
3. In the Elements tab, look for each input field
4. Find the `name` attribute - it will look like: `entry.123456789`
5. Record the entry ID for each field:

```
Creator Name field:  entry.XXXXXXXXX
Email field:         entry.XXXXXXXXX
Photo field:         entry.XXXXXXXXX
```

### Method 2: Pre-fill Form URL
1. Click the **More** menu (⋮) in the form editor
2. Select **Get pre-filled link**
3. Fill out the form with test data
4. Click **Get link**
5. Copy the URL - the entry IDs are visible in the URL parameters

## Step 5: Get Form Action URL

1. Click the **Preview** button (eye icon) to open the form
2. Right-click on the page → **Inspect** (or press F12)
3. In the Elements tab, find the `<form>` tag near the top
4. Look for the `action` attribute - it will look like:
   ```
   https://docs.google.com/forms/d/e/XXXXX_FORM_ID_XXXXX/formResponse
   ```
5. Copy this entire URL

## Step 6: Update the Creator Portal Code

Open `atlas-portal/script.js` and find the `GOOGLE_FORM_CONFIG` object near the top of the file.

Replace the placeholder values with your actual form data:

```javascript
const GOOGLE_FORM_CONFIG = {
    actionUrl: 'https://docs.google.com/forms/d/e/YOUR_FORM_ID/formResponse',
    fields: {
        creatorName: 'entry.123456789',  // Replace with your actual entry ID
        email: 'entry.987654321',        // Replace with your actual entry ID
        photo: 'entry.555555555'         // Replace with your actual entry ID
    }
};
```

## Step 7: Test the Integration

1. Open the creator portal in your browser
2. Fill in your name and email
3. Upload a test photo
4. Generate a graphic
5. Download the graphic (this triggers the form submission)
6. Check your Google Form responses to verify the data was received

### Troubleshooting

**Issue**: Submissions not appearing in Google Form
- **Solution**: Check that the entry IDs are correct
- **Solution**: Verify the form action URL is complete and correct
- **Solution**: Make sure file uploads are enabled in the form settings

**Issue**: File upload requires login
- **Solution**: This is normal - Google Forms file uploads require authentication
- **Solution**: Consider using an alternative method (e.g., email submission) if login is a barrier

**Issue**: CORS errors in browser console
- **Solution**: This is expected - we use `mode: 'no-cors'` to bypass CORS restrictions
- **Solution**: The form will still receive submissions despite the CORS error

## Step 8: View Responses

View submitted data in several ways:

### Option 1: Responses Tab
1. Go to your Google Form
2. Click the **Responses** tab
3. See submissions in a table or individual format

### Option 2: Google Sheets
1. In the Responses tab, click the Google Sheets icon
2. This creates a spreadsheet with all responses
3. Photos will be linked (clickable URLs)

### Option 3: View Files
1. Go to Google Drive
2. Find the folder: "[Form Name] (Responses)"
3. All uploaded photos are stored here
4. Files are organized by submission

## Privacy & Data Handling

### What Data is Collected
- Creator name (optional)
- Email address (optional)
- Profile photo (if uploaded)
- Timestamp of submission

### Data Usage
- Photos may be used in creator profiles on the Atlas
- Email addresses are only used to contact creators about their photos
- No data is shared with third parties

### User Consent
- The disclosure box clearly states photos may be used in Atlas profiles
- Uploading is completely optional
- Users can opt to use a placeholder avatar instead

### GDPR/Privacy Considerations
- ✅ Clear disclosure before data collection
- ✅ Optional submission (not required to use the tool)
- ✅ Explicit purpose stated (profile photos)
- ✅ Limited data collection (only name, email, photo)
- ⚠️ Consider adding a privacy policy link
- ⚠️ Consider adding a data deletion request process

## Alternative: Email-Based Submission

If Google Forms file upload is too restrictive, consider an alternative approach:

### Option A: Email Submission
Instead of Google Forms, send data via email using a service like:
- Formspree (form backend service)
- EmailJS (client-side email)
- Netlify Forms (if hosted on Netlify)

### Option B: Cloud Storage
Upload photos directly to:
- AWS S3 (with pre-signed URLs)
- Cloudinary (image hosting service)
- Firebase Storage
- Then submit metadata to Google Forms

## Sample Google Form Structure

Here's what your form should look like:

```
════════════════════════════════════════════════════
Atlas Creator Photo Collection
────────────────────────────────────────────────────
Help us build better creator profiles!
════════════════════════════════════════════════════

1. Your Name
   [                                              ]
   What name should we use to identify you?

2. Email Address
   [                                              ]
   We'll only contact you about using your photo

3. Your Photo
   [📎 Choose file] No file chosen
   Upload a square photo (500x500px or larger)

                                         [Submit]
════════════════════════════════════════════════════
```

## Next Steps

After setup is complete:

1. ✅ Test the form submission flow end-to-end
2. ✅ Monitor initial submissions for data quality
3. ✅ Set up email notifications for new submissions
4. ✅ Create a process for reviewing and approving photos
5. ✅ Document how to add photos to creator profiles
6. ⚠️ Consider adding a follow-up email to thank submitters
7. ⚠️ Track submission rate to measure feature adoption

---

**Need Help?**
- Google Forms Help Center: https://support.google.com/docs/topic/9054603
- File Upload in Forms: https://support.google.com/docs/answer/7322334

**Questions about Implementation?**
- Check the creator portal README.md
- Review the script.js comments for technical details
- Test in a development environment first

---

**Version**: 1.0
**Last Updated**: February 2025
