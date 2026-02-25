# Creator Portal Setup Checklist

Quick reference for completing the photo collection feature setup.

## ✅ Already Complete

- [x] HTML structure with creator info fields
- [x] Disclosure box explaining photo usage
- [x] JavaScript photo submission logic
- [x] Form validation
- [x] Auto-submission on download
- [x] Clear, friendly copy
- [x] Responsive design
- [x] Error handling

## 🔧 To Do: Create Google Form

### Step 1: Create the Form
1. Go to [forms.google.com](https://forms.google.com)
2. Create new form: "Atlas Creator Photo Collection"
3. Add these fields **in order**:

#### Field 1: Your Name
- Type: Short answer
- Question: "Your Name"
- Description: "What name should we use to identify you?"
- Required: **No** (optional)

#### Field 2: Email Address
- Type: Short answer (or Email with validation)
- Question: "Email Address"
- Description: "We'll only contact you about using your photo in your Atlas profile"
- Required: **No** (optional)

#### Field 3: Your Photo
- Type: **File upload**
- Question: "Your Photo"
- Description: "Upload a square photo (500x500px or larger recommended)"
- Settings:
  - Allow: Images only (JPG, PNG)
  - Max size: 10 MB
  - Max files: 1
- Required: **No** (optional)

### Step 2: Configure Form Settings
- Go to Settings (⚙️ icon)
- Responses tab:
  - ✅ Collect email addresses (recommended)
  - ✅ Limit to 1 response (optional)
- Presentation tab:
  - Set confirmation message: "Thank you! We received your photo and will be in touch if we'd like to use it in your Atlas profile."

### Step 3: Get Entry IDs
1. Click Preview (👁️ icon)
2. Right-click → Inspect (F12)
3. Find each input's `name` attribute (looks like: `entry.123456789`)
4. Record all three entry IDs:
   ```
   Name field:  entry.__________
   Email field: entry.__________
   Photo field: entry.__________
   ```

### Step 4: Get Form Action URL
1. In Preview mode, inspect the page
2. Find the `<form>` tag
3. Copy the `action` attribute URL (looks like: `https://docs.google.com/forms/d/e/[FORM_ID]/formResponse`)

### Step 5: Update the Code
Edit `atlas-portal/script.js` and update `GOOGLE_FORM_CONFIG`:

```javascript
const GOOGLE_FORM_CONFIG = {
    actionUrl: 'https://docs.google.com/forms/d/e/[YOUR_FORM_ID]/formResponse',
    fields: {
        creatorName: 'entry.123456789',  // Replace with your entry ID
        email: 'entry.987654321',        // Replace with your entry ID
        photo: 'entry.555555555'         // Replace with your entry ID
    }
};
```

### Step 6: Test It!
1. Open `atlas-portal/index.html`
2. Enter name and email
3. Upload a test photo
4. Generate graphic
5. Download graphic (this submits the form)
6. Check Google Form responses

## 📋 Quick Reference Files

- **Detailed instructions**: `GOOGLE_FORM_SETUP.md`
- **Form template mockup**: `google-form-template.html`
- **Portal documentation**: `README.md`
- **Code to update**: `script.js` (line ~18-30)

## 🔍 How to Verify It's Working

1. Open browser console (F12)
2. Download a graphic
3. Look for: `"Photo submission sent to Google Form"`
4. Check Google Form responses tab
5. Verify data appears correctly

## ⚠️ Important Notes

- **File uploads require Google login**: Users must sign in to upload files
- **CORS is expected**: You'll see CORS errors in console, but form still works
- **Optional fields**: All fields are optional - submission only happens if photo is uploaded
- **Silent failure**: If form isn't configured, submission fails silently (won't break user experience)
- **Privacy**: Clear disclosure is shown before photo upload

## 📞 Troubleshooting

| Issue | Solution |
|-------|----------|
| No submissions appearing | Check entry IDs are correct |
| CORS errors | Normal - use `no-cors` mode |
| File upload not working | Verify file upload is enabled in form |
| Form not submitting | Check action URL is complete |
| Users can't upload | They need to be signed in to Google |

## 🎯 Success Criteria

✅ Users see disclosure before uploading
✅ Name and email fields work
✅ Photo uploads successfully
✅ Download triggers form submission
✅ Data appears in Google Form responses
✅ Users receive confirmation message
✅ No errors that break user experience

---

**Ready to go?** Start with Step 1 above, then follow `GOOGLE_FORM_SETUP.md` for detailed instructions.

**Questions?** Check the troubleshooting section or review the code comments in `script.js`.
