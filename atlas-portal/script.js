// Creator Portal - Social Graphic Generator
// Independent Journalism Atlas

(function() {
    'use strict';

    // State
    const state = {
        uploadedImage: null,
        usePlaceholder: false,
        selectedMessage: 'message1',
        customMessage: '',
        backgroundColor: '#000000',
        textColor: '#FFFFFF',
        generated: false,
        logoImages: {} // Will store preloaded logo images
    };

    // Pre-written messages
    const messages = {
        message1: "I'm in the Independent Journalism Atlas—a searchable database of independent journalists across platforms. Explore more at journalismatlas.com",
        message2: "Proud to be included in the Independent Journalism Atlas alongside 1,000+ independent journalists doing this work across YouTube, Substack, Instagram, Beehiiv, TikTok, Bluesky, X and more.",
        message3: "The Independent Journalism Atlas is mapping the creator journalism ecosystem. I'm in it -- alongside over 1,000 others at journalismatlas.com",
        message4: "Independent journalism is thriving across platforms, and the Independent Journalism Atlas is mapping it. Honored to be included."
    };

    // Google Form Configuration
    // INSTRUCTIONS: Replace with your actual Google Form action URL
    const GOOGLE_FORM_CONFIG = {
        // Step 1: Create a Google Form with these fields:
        // - Creator Name (Short answer)
        // - Email (Email field)
        // - Photo Upload (File upload)
        // - Timestamp (automatically captured)

        // Step 2: Get the form action URL from your Google Form
        // (Right-click form > Inspect > Find the <form> tag > Copy the 'action' attribute)
        actionUrl: 'YOUR_GOOGLE_FORM_URL_HERE',

        // Step 3: Get the field entry IDs from your Google Form
        // (Inspect each input field and find the 'name' attribute, e.g., "entry.123456789")
        fields: {
            creatorName: 'entry.XXXXXXXX',  // Replace with actual entry ID
            email: 'entry.XXXXXXXX',        // Replace with actual entry ID
            // Note: File upload in Google Forms requires special handling
            // The photo will need to be converted to a data URL or uploaded separately
        }
    };

    // DOM Elements
    const elements = {
        photoUpload: document.getElementById('photoUpload'),
        imagePreview: document.getElementById('imagePreview'),
        previewImg: document.getElementById('previewImg'),
        usePlaceholder: document.getElementById('usePlaceholder'),
        creatorName: document.getElementById('creatorName'),
        creatorEmail: document.getElementById('creatorEmail'),
        messageOptions: document.querySelectorAll('input[name="message"]'),
        customMessageGroup: document.getElementById('customMessageGroup'),
        customMessage: document.getElementById('customMessage'),
        charCounter: document.getElementById('charCounter'),
        bgColorOptions: document.querySelectorAll('#bgColorSelector .color-option'),
        textColorOptions: document.querySelectorAll('#textColorSelector .text-color-option'),
        previewCanvas: document.getElementById('previewCanvas'),
        generateBtn: document.getElementById('generateBtn'),
        downloadButtons: document.getElementById('downloadButtons'),
        downloadSquare: document.getElementById('downloadSquare'),
        downloadWide: document.getElementById('downloadWide'),
        generateMessage: document.getElementById('generateMessage'),
        radioOptions: document.querySelectorAll('.radio-option'),
        captionSection: document.getElementById('captionSection'),
        captionText: document.getElementById('captionText'),
        copyCaptionBtn: document.getElementById('copyCaptionBtn'),
        copyBtnText: document.getElementById('copyBtnText')
    };

    // Initialize
    function init() {
        setupEventListeners();
        loadLogos(); // Load logo images
        updatePreview();
        setupNavScroll();
    }

    // Load logo images
    function loadLogos() {
        // Define logo paths for different backgrounds
        const logoSources = {
            // For dark backgrounds (black, dark gray, olive green)
            whiteIcon: '../assets/images/icons/Journalism_Atlas_icon_white_transparent.png',
            whiteWordmark: '../assets/images/logos/Journalism_Atlas_wordmark_lockup_white.png',

            // For light backgrounds (acid green, lime green)
            blackIcon: '../assets/images/icons/Journalism_Atlas_icon_black_transparent.png',
            blackWordmark: '../assets/images/logos/Journalism_Atlas_wordmark_lockup_black.png'
        };

        // Preload all logo images
        Object.keys(logoSources).forEach(key => {
            const img = new Image();
            img.onload = function() {
                state.logoImages[key] = img;
                // Update preview once logos are loaded
                if (Object.keys(state.logoImages).length === Object.keys(logoSources).length) {
                    updatePreview();
                }
            };
            img.onerror = function() {
                console.error(`Failed to load logo: ${logoSources[key]}`);
            };
            img.src = logoSources[key];
        });
    }

    // Get appropriate logo color based on background
    function getLogoType(backgroundColor) {
        // Light backgrounds need black logos
        const lightBackgrounds = ['#ceff00', '#97d600'];

        if (lightBackgrounds.includes(backgroundColor)) {
            return 'black';
        } else {
            // Dark backgrounds (black, dark gray, olive green) need white logos
            return 'white';
        }
    }

    // Setup all event listeners
    function setupEventListeners() {
        // Photo upload
        elements.photoUpload.addEventListener('change', handlePhotoUpload);
        elements.usePlaceholder.addEventListener('change', handlePlaceholderToggle);

        // Message selection
        elements.messageOptions.forEach(radio => {
            radio.addEventListener('change', handleMessageChange);
        });

        // Custom message
        elements.customMessage.addEventListener('input', handleCustomMessageInput);

        // Color selection
        elements.bgColorOptions.forEach(option => {
            option.addEventListener('click', () => selectBackgroundColor(option));
        });

        elements.textColorOptions.forEach(option => {
            option.addEventListener('click', () => selectTextColor(option));
        });

        // Generate and download
        elements.generateBtn.addEventListener('click', handleGenerate);
        elements.downloadSquare.addEventListener('click', () => downloadImage('square'));
        elements.downloadWide.addEventListener('click', () => downloadImage('wide'));

        // Copy caption
        elements.copyCaptionBtn.addEventListener('click', handleCopyCaption);

        // Radio option styling
        elements.radioOptions.forEach(option => {
            option.addEventListener('click', function() {
                elements.radioOptions.forEach(opt => opt.classList.remove('selected'));
                this.classList.add('selected');
            });
        });
    }

    // Setup navigation scroll effect
    function setupNavScroll() {
        const nav = document.querySelector('.top-nav');
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });
    }

    // Handle photo upload
    function handlePhotoUpload(e) {
        const file = e.target.files[0];
        if (!file) return;

        // Validate file type
        if (!file.type.match('image/(jpeg|jpg|png)')) {
            showMessage('error', 'Please upload a JPG or PNG image.');
            return;
        }

        // Validate file size (5MB max)
        if (file.size > 5 * 1024 * 1024) {
            showMessage('error', 'File size must be under 5MB.');
            return;
        }

        const reader = new FileReader();
        reader.onload = function(event) {
            const img = new Image();
            img.onload = function() {
                state.uploadedImage = img;
                elements.previewImg.src = event.target.result;
                elements.imagePreview.classList.add('visible');
                elements.usePlaceholder.checked = false;
                state.usePlaceholder = false;
                updatePreview();
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);
    }

    // Handle placeholder toggle
    function handlePlaceholderToggle(e) {
        state.usePlaceholder = e.target.checked;
        if (e.target.checked) {
            elements.imagePreview.classList.remove('visible');
            elements.photoUpload.value = '';
            state.uploadedImage = null;
        }
        updatePreview();
    }

    // Handle message selection
    function handleMessageChange(e) {
        state.selectedMessage = e.target.value;

        if (e.target.value === 'custom') {
            elements.customMessageGroup.classList.remove('hidden');
            elements.customMessage.focus();
        } else {
            elements.customMessageGroup.classList.add('hidden');
        }

        updatePreview();
    }

    // Handle custom message input
    function handleCustomMessageInput(e) {
        const remaining = 280 - e.target.value.length;
        state.customMessage = e.target.value;

        elements.charCounter.textContent = `${remaining} characters remaining`;

        if (remaining < 20) {
            elements.charCounter.classList.add('warning');
        } else {
            elements.charCounter.classList.remove('warning');
        }

        if (remaining < 0) {
            elements.charCounter.classList.add('error');
            elements.charCounter.classList.remove('warning');
        } else {
            elements.charCounter.classList.remove('error');
        }

        updatePreview();
    }

    // Select background color
    function selectBackgroundColor(option) {
        elements.bgColorOptions.forEach(opt => opt.classList.remove('selected'));
        option.classList.add('selected');
        state.backgroundColor = option.dataset.color;
        updatePreview();
    }

    // Select text color
    function selectTextColor(option) {
        elements.textColorOptions.forEach(opt => opt.classList.remove('selected'));
        option.classList.add('selected');
        state.textColor = option.dataset.color;
        updatePreview();
    }

    // Get current message text
    function getCurrentMessage() {
        if (state.selectedMessage === 'custom') {
            return state.customMessage || '';
        }
        return messages[state.selectedMessage] || '';
    }

    // Update preview canvas
    function updatePreview() {
        renderCanvas(elements.previewCanvas, 1080, 1080, true);
    }

    // Handle generate button
    function handleGenerate() {
        const message = getCurrentMessage();

        if (!message.trim()) {
            showMessage('error', 'Please select a message or write your own.');
            return;
        }

        if (state.selectedMessage === 'custom' && message.length > 280) {
            showMessage('error', 'Custom message must be 280 characters or less.');
            return;
        }

        state.generated = true;
        elements.downloadButtons.classList.remove('hidden');

        // Show caption section and populate it
        showCaption(message);

        showMessage('success', 'Graphic generated! Click below to download.');

        // Scroll to download buttons
        elements.downloadButtons.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // Show and populate caption section
    function showCaption(message) {
        // Create caption with message and hashtags
        const caption = `${message}\n\n#IndependentJournalism #CreatorEconomy`;

        // Display caption
        elements.captionText.textContent = caption;
        elements.captionSection.classList.add('visible');
    }

    // Handle copy caption button
    function handleCopyCaption() {
        const caption = elements.captionText.textContent;

        // Try to copy to clipboard
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(caption).then(() => {
                // Success feedback
                elements.copyBtnText.textContent = '✓ Copied!';
                elements.copyCaptionBtn.classList.add('copied');

                // Reset button after 2 seconds
                setTimeout(() => {
                    elements.copyBtnText.textContent = '📋 Copy Caption';
                    elements.copyCaptionBtn.classList.remove('copied');
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy:', err);
                showMessage('error', 'Failed to copy. Please select and copy the text manually.');
            });
        } else {
            // Fallback: Select the text for manual copying
            const range = document.createRange();
            range.selectNodeContents(elements.captionText);
            const selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);

            // Try execCommand as fallback
            try {
                document.execCommand('copy');
                elements.copyBtnText.textContent = '✓ Copied!';
                elements.copyCaptionBtn.classList.add('copied');

                setTimeout(() => {
                    elements.copyBtnText.textContent = '📋 Copy Caption';
                    elements.copyCaptionBtn.classList.remove('copied');
                }, 2000);
            } catch (err) {
                showMessage('error', 'Please select and copy the text manually.');
            }
        }
    }

    // Render canvas
    function renderCanvas(canvas, width, height, isSquare = true) {
        const ctx = canvas.getContext('2d');
        canvas.width = width;
        canvas.height = height;

        // Clear canvas
        ctx.clearRect(0, 0, width, height);

        // Background
        ctx.fillStyle = state.backgroundColor;
        ctx.fillRect(0, 0, width, height);

        // Get message
        const message = getCurrentMessage();

        if (isSquare) {
            // Square format (1080x1080) - Instagram
            renderSquareFormat(ctx, width, height, message);
        } else {
            // Wide format (1200x630) - Twitter/LinkedIn
            renderWideFormat(ctx, width, height, message);
        }
    }

    // Render square format (1080x1080)
    function renderSquareFormat(ctx, width, height, message) {
        const centerX = width / 2;

        // Draw profile photo
        const photoSize = 300;
        const photoY = 200;

        if (state.uploadedImage) {
            drawCircularImage(ctx, state.uploadedImage, centerX, photoY + photoSize / 2, photoSize / 2);
        } else if (state.usePlaceholder) {
            drawPlaceholderAvatar(ctx, centerX, photoY + photoSize / 2, photoSize / 2);
        }

        // Draw message text
        ctx.fillStyle = state.textColor;
        ctx.font = '600 36px Hanken Grotesk, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';

        const textY = 570;
        const maxWidth = 900;
        const lineHeight = 54;

        wrapText(ctx, message, centerX, textY, maxWidth, lineHeight);

        // Draw URL at bottom center
        ctx.font = '400 20px Hanken Grotesk, sans-serif';
        ctx.fillStyle = state.textColor;
        ctx.globalAlpha = 0.8;
        ctx.fillText('journalismatlas.com', centerX, height - 50);
        ctx.globalAlpha = 1;

        // Draw logo (bottom right corner)
        drawAtlasLogo(ctx, width, height, 'square');
    }

    // Render wide format (1200x630)
    function renderWideFormat(ctx, width, height, message) {
        // Draw profile photo (left side)
        const photoSize = 200;
        const photoX = 100;
        const photoY = height / 2;

        if (state.uploadedImage) {
            drawCircularImage(ctx, state.uploadedImage, photoX + photoSize / 2, photoY, photoSize / 2);
        } else if (state.usePlaceholder) {
            drawPlaceholderAvatar(ctx, photoX + photoSize / 2, photoY, photoSize / 2);
        }

        // Draw message text (right side)
        ctx.fillStyle = state.textColor;
        ctx.font = '600 32px Hanken Grotesk, sans-serif';
        ctx.textAlign = 'left';
        ctx.textBaseline = 'middle';

        const textX = 350;
        const textY = height / 2;
        const maxWidth = 750;
        const lineHeight = 48;

        wrapText(ctx, message, textX, textY - 60, maxWidth, lineHeight, 'left');

        // Draw URL at bottom left
        ctx.font = '400 18px Hanken Grotesk, sans-serif';
        ctx.fillStyle = state.textColor;
        ctx.globalAlpha = 0.8;
        ctx.textAlign = 'left';
        ctx.fillText('journalismatlas.com', 40, height - 40);
        ctx.globalAlpha = 1;

        // Draw logo (bottom right corner)
        drawAtlasLogo(ctx, width, height, 'wide');
    }

    // Draw circular image
    function drawCircularImage(ctx, img, x, y, radius) {
        ctx.save();
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.closePath();
        ctx.clip();

        // Calculate dimensions to cover the circle
        const imgAspect = img.width / img.height;
        let drawWidth, drawHeight, offsetX, offsetY;

        if (imgAspect > 1) {
            // Image is wider
            drawHeight = radius * 2;
            drawWidth = drawHeight * imgAspect;
            offsetX = x - drawWidth / 2;
            offsetY = y - radius;
        } else {
            // Image is taller or square
            drawWidth = radius * 2;
            drawHeight = drawWidth / imgAspect;
            offsetX = x - radius;
            offsetY = y - drawHeight / 2;
        }

        ctx.drawImage(img, offsetX, offsetY, drawWidth, drawHeight);
        ctx.restore();

        // Draw border
        ctx.strokeStyle = state.textColor;
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.stroke();
    }

    // Draw placeholder avatar
    function drawPlaceholderAvatar(ctx, x, y, radius) {
        // Circle background
        ctx.fillStyle = state.textColor;
        ctx.globalAlpha = 0.2;
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;

        // Simple person icon
        ctx.fillStyle = state.textColor;
        ctx.globalAlpha = 0.5;

        // Head
        ctx.beginPath();
        ctx.arc(x, y - radius * 0.15, radius * 0.3, 0, Math.PI * 2);
        ctx.fill();

        // Body
        ctx.beginPath();
        ctx.arc(x, y + radius * 0.6, radius * 0.5, 0, Math.PI * 2);
        ctx.fill();

        ctx.globalAlpha = 1;

        // Border
        ctx.strokeStyle = state.textColor;
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.stroke();
    }

    // Wrap text
    function wrapText(ctx, text, x, y, maxWidth, lineHeight, align = 'center') {
        const words = text.split(' ');
        let line = '';
        const lines = [];

        for (let i = 0; i < words.length; i++) {
            const testLine = line + words[i] + ' ';
            const metrics = ctx.measureText(testLine);
            const testWidth = metrics.width;

            if (testWidth > maxWidth && i > 0) {
                lines.push(line);
                line = words[i] + ' ';
            } else {
                line = testLine;
            }
        }
        lines.push(line);

        // Calculate starting Y position to center the text block
        const totalHeight = lines.length * lineHeight;
        let startY = y;

        if (align === 'center') {
            startY = y - totalHeight / 2 + lineHeight / 2;
        }

        // Draw each line
        lines.forEach((line, index) => {
            ctx.fillText(line.trim(), x, startY + index * lineHeight);
        });
    }

    // Draw Atlas logo (icon + wordmark)
    function drawAtlasLogo(ctx, canvasWidth, canvasHeight, format) {
        const logoType = getLogoType(state.backgroundColor);
        const icon = state.logoImages[`${logoType}Icon`];
        const wordmark = state.logoImages[`${logoType}Wordmark`];

        // Check if logos are loaded
        if (!icon || !wordmark) {
            // Fallback to simple placeholder if logos aren't loaded yet
            drawLogoPlaceholder(ctx, canvasWidth - 70, canvasHeight - 70, 50);
            return;
        }

        if (format === 'square') {
            // Square format (1080x1080) - Stack icon above wordmark in corner
            const iconSize = 50;
            const wordmarkWidth = 120;
            const wordmarkHeight = (wordmarkWidth / wordmark.width) * wordmark.height;
            const padding = 30;

            // Position in bottom right
            const iconX = canvasWidth - padding - iconSize / 2;
            const iconY = canvasHeight - padding - iconSize - wordmarkHeight - 10;

            // Draw icon
            ctx.globalAlpha = 0.9;
            ctx.drawImage(icon, iconX - iconSize / 2, iconY - iconSize / 2, iconSize, iconSize);

            // Draw wordmark below icon
            const wordmarkX = canvasWidth - padding - wordmarkWidth / 2;
            const wordmarkY = canvasHeight - padding - wordmarkHeight;
            ctx.drawImage(wordmark, wordmarkX - wordmarkWidth / 2, wordmarkY, wordmarkWidth, wordmarkHeight);
            ctx.globalAlpha = 1;

        } else {
            // Wide format (1200x630) - Side by side layout
            const iconSize = 45;
            const wordmarkHeight = 35;
            const wordmarkWidth = (wordmarkHeight / wordmark.height) * wordmark.width;
            const padding = 25;
            const gap = 10;

            // Position in bottom right
            const totalWidth = iconSize + gap + wordmarkWidth;
            const iconX = canvasWidth - padding - totalWidth + iconSize / 2;
            const iconY = canvasHeight - padding - iconSize / 2;

            // Draw icon
            ctx.globalAlpha = 0.9;
            ctx.drawImage(icon, iconX - iconSize / 2, iconY - iconSize / 2, iconSize, iconSize);

            // Draw wordmark to the right of icon
            const wordmarkX = iconX + iconSize / 2 + gap;
            const wordmarkY = iconY - wordmarkHeight / 2;
            ctx.drawImage(wordmark, wordmarkX, wordmarkY, wordmarkWidth, wordmarkHeight);
            ctx.globalAlpha = 1;
        }
    }

    // Draw logo placeholder (fallback if images don't load)
    function drawLogoPlaceholder(ctx, x, y, size) {
        ctx.fillStyle = state.textColor;
        ctx.globalAlpha = 0.3;
        ctx.beginPath();
        ctx.arc(x, y, size / 2, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;

        // Atlas "A" placeholder
        ctx.fillStyle = state.textColor;
        ctx.globalAlpha = 0.6;
        ctx.font = `bold ${size * 0.6}px Hanken Grotesk, sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('A', x, y);
        ctx.globalAlpha = 1;
    }

    // Download image
    function downloadImage(format) {
        if (!state.generated) {
            showMessage('error', 'Please generate your graphic first.');
            return;
        }

        const message = getCurrentMessage();
        if (!message.trim()) {
            showMessage('error', 'Please select a message or write your own.');
            return;
        }

        // Create temporary canvas for download
        const downloadCanvas = document.createElement('canvas');

        if (format === 'square') {
            renderCanvas(downloadCanvas, 1080, 1080, true);
        } else {
            renderCanvas(downloadCanvas, 1200, 630, false);
        }

        // Convert to blob and download
        downloadCanvas.toBlob(blob => {
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            const timestamp = Date.now();
            const formatName = format === 'square' ? '1080x1080' : '1200x630';

            link.download = `atlas-share-${formatName}-${timestamp}.png`;
            link.href = url;
            link.click();

            URL.revokeObjectURL(url);

            showMessage('success', `Downloaded ${formatName} graphic!`);

            // Submit photo to Google Form if user uploaded a photo and provided name
            submitPhotoToGoogleForm();
        }, 'image/png');
    }

    // Submit photo data to Google Form
    function submitPhotoToGoogleForm() {
        // Check if user uploaded a photo (not using placeholder)
        if (!state.uploadedImage || state.usePlaceholder) {
            return; // No photo to submit
        }

        // Get creator info
        const creatorName = elements.creatorName.value.trim();
        const creatorEmail = elements.creatorEmail.value.trim();

        // Only submit if we have at least a name or email
        if (!creatorName && !creatorEmail) {
            return; // No identifying info provided
        }

        // Check if Google Form is configured
        if (GOOGLE_FORM_CONFIG.actionUrl === 'YOUR_GOOGLE_FORM_URL_HERE') {
            console.log('Google Form not configured. Skipping photo submission.');
            console.log('Photo submission would include:', {
                name: creatorName,
                email: creatorEmail,
                hasPhoto: true
            });
            return;
        }

        // Create form data
        const formData = new FormData();

        // Add creator info to form
        if (creatorName) {
            formData.append(GOOGLE_FORM_CONFIG.fields.creatorName, creatorName);
        }

        if (creatorEmail) {
            formData.append(GOOGLE_FORM_CONFIG.fields.email, creatorEmail);
        }

        // Convert uploaded image to blob and add to form
        // Note: This assumes the Google Form has a file upload field configured
        if (state.uploadedImage && elements.photoUpload.files[0]) {
            formData.append(GOOGLE_FORM_CONFIG.fields.photo, elements.photoUpload.files[0]);
        }

        // Submit to Google Form using fetch (no-cors mode for cross-origin)
        fetch(GOOGLE_FORM_CONFIG.actionUrl, {
            method: 'POST',
            mode: 'no-cors',
            body: formData
        }).then(() => {
            console.log('Photo submission sent to Google Form');
            // Note: Due to no-cors mode, we can't verify if submission succeeded
            // But Google Forms will accept it if properly configured
        }).catch(error => {
            console.error('Error submitting photo:', error);
            // Fail silently - don't disrupt user experience
        });
    }

    // Show message
    function showMessage(type, text) {
        elements.generateMessage.className = `message ${type} visible`;
        elements.generateMessage.textContent = text;

        // Auto-hide after 5 seconds
        setTimeout(() => {
            elements.generateMessage.classList.remove('visible');
        }, 5000);
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
