// API Base URL - change this if your backend runs on a different port
const API_BASE_URL = 'http://localhost:8000';

// Global variables to store uploaded files
let referenceFiles = {};
let classifyFile = null;

// Utility function to show/hide elements
function showElement(id) {
    document.getElementById(id).classList.remove('hidden');
}

function hideElement(id) {
    document.getElementById(id).classList.add('hidden');
}

// Handle reference image uploads
function handleReferenceUpload(index, input) {
    const file = input.files[0];
    if (file) {
        referenceFiles[index] = file;
        
        // Show preview
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById(`ref${index}-img`).src = e.target.result;
            showElement(`ref${index}-preview`);
            hideElement(`ref${index}-placeholder`);
        };
        reader.readAsDataURL(file);
    }
}

// Handle classify image upload
function handleClassifyUpload(input) {
    const file = input.files[0];
    if (file) {
        classifyFile = file;
        
        // Show preview
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('classify-img').src = e.target.result;
            showElement('classify-preview');
            hideElement('classify-placeholder');
        };
        reader.readAsDataURL(file);
    }
}

// Upload reference images to backend
async function uploadReferences() {
    // Check if all 4 images and captions are provided
    const requiredFiles = [1, 2, 3, 4];
    const missingFiles = requiredFiles.filter(i => !referenceFiles[i]);
    
    if (missingFiles.length > 0) {
        showStatus('Please upload all 4 reference images', 'error');
        return;
    }
    
    // Check captions
    const captions = [];
    for (let i = 1; i <= 4; i++) {
        const caption = document.getElementById(`caption${i}`).value.trim();
        if (!caption) {
            showStatus(`Please enter caption for reference image ${i}`, 'error');
            return;
        }
        captions.push(caption);
    }
    
    // Prepare form data
    const formData = new FormData();
    
    // Add files
    for (let i = 1; i <= 4; i++) {
        formData.append('files', referenceFiles[i]);
    }
    
    // Add captions
    captions.forEach(caption => {
        formData.append('captions', caption);
    });
    
    try {
        showStatus('Uploading reference images...', 'loading');
        
        const response = await fetch(`${API_BASE_URL}/upload_references`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showStatus(`✅ ${result.message}`, 'success');
        } else {
            showStatus(`❌ Error: ${result.detail}`, 'error');
        }
    } catch (error) {
        console.error('Error uploading references:', error);
        showStatus('❌ Failed to upload references. Make sure the backend is running.', 'error');
    }
}

// Classify uploaded image
async function classifyImage() {
    if (!classifyFile) {
        alert('Please upload an image first');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', classifyFile);
    
    try {
        // Show loading state
        hideElement('classification-result');
        hideElement('description-result');
        showElement('loading-classify');
        
        const response = await fetch(`${API_BASE_URL}/classify`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        hideElement('loading-classify');
        
        if (response.ok) {
            // Display classification result
            document.getElementById('classification-label').textContent = result.label;
            document.getElementById('confidence-score').textContent = `${(result.similarity * 100).toFixed(1)}%`;
            
            // Update card style based on result
            const resultCard = document.querySelector('#classification-result .result-card');
            resultCard.className = 'result-card text-white p-4 rounded-lg';
            
            if (result.label === 'Rare Event') {
                resultCard.classList.add('rare-event');
            } else {
                resultCard.classList.add('normal-event');
            }
            
            showElement('classification-result');
        } else {
            alert(`Error: ${result.detail}`);
        }
    } catch (error) {
        hideElement('loading-classify');
        console.error('Error classifying image:', error);
        alert('Failed to classify image. Make sure the backend is running.');
    }
}

// Describe uploaded image
async function describeImage() {
    if (!classifyFile) {
        alert('Please upload an image first');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', classifyFile);
    
    try {
        // Show loading state
        hideElement('classification-result');
        hideElement('description-result');
        showElement('loading-describe');
        
        const response = await fetch(`${API_BASE_URL}/describe`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        hideElement('loading-describe');
        
        if (response.ok) {
            // Display description result
            document.getElementById('description-text').textContent = result.description;
            showElement('description-result');
        } else {
            alert(`Error: ${result.detail}`);
        }
    } catch (error) {
        hideElement('loading-describe');
        console.error('Error describing image:', error);
        alert('Failed to describe image. Make sure the backend is running.');
    }
}

// Generate synthetic image
async function generateImage() {
    const caption = document.getElementById('generation-caption').value.trim();
    
    if (!caption) {
        alert('Please enter a caption for image generation');
        return;
    }
    
    const formData = new FormData();
    formData.append('caption', caption);
    
    try {
        // Show loading state
        hideElement('generated-result');
        showElement('loading-generate');
        
        const response = await fetch(`${API_BASE_URL}/generate`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        hideElement('loading-generate');
        
        if (response.ok) {
            // Display generated image
            document.getElementById('generated-image').src = result.image;
            document.getElementById('generated-caption').textContent = `Generated: "${result.caption}"`;
            showElement('generated-result');
        } else {
            alert(`Error: ${result.detail}`);
        }
    } catch (error) {
        hideElement('loading-generate');
        console.error('Error generating image:', error);
        alert('Failed to generate image. Make sure the backend is running.');
    }
}

// Show status messages
function showStatus(message, type) {
    const statusElement = document.getElementById('upload-status');
    statusElement.textContent = message;
    
    // Remove existing classes
    statusElement.className = 'mt-4 text-center';
    
    // Add appropriate styling
    switch (type) {
        case 'success':
            statusElement.classList.add('text-green-600', 'font-semibold');
            break;
        case 'error':
            statusElement.classList.add('text-red-600', 'font-semibold');
            break;
        case 'loading':
            statusElement.classList.add('text-blue-600', 'font-semibold');
            break;
        default:
            statusElement.classList.add('text-gray-600');
    }
    
    showElement('upload-status');
    
    // Auto-hide after 5 seconds for non-error messages
    if (type !== 'error') {
        setTimeout(() => {
            hideElement('upload-status');
        }, 5000);
    }
}

// Add drag and drop functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add drag and drop for all upload areas
    const uploadAreas = document.querySelectorAll('.upload-area');
    
    uploadAreas.forEach(area => {
        area.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('dragover');
        });
        
        area.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
        });
        
        area.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                const file = files[0];
                
                // Determine which upload area this is
                if (this.onclick.toString().includes('ref1')) {
                    document.getElementById('ref1').files = files;
                    handleReferenceUpload(1, document.getElementById('ref1'));
                } else if (this.onclick.toString().includes('ref2')) {
                    document.getElementById('ref2').files = files;
                    handleReferenceUpload(2, document.getElementById('ref2'));
                } else if (this.onclick.toString().includes('ref3')) {
                    document.getElementById('ref3').files = files;
                    handleReferenceUpload(3, document.getElementById('ref3'));
                } else if (this.onclick.toString().includes('ref4')) {
                    document.getElementById('ref4').files = files;
                    handleReferenceUpload(4, document.getElementById('ref4'));
                } else if (this.onclick.toString().includes('classify-image')) {
                    document.getElementById('classify-image').files = files;
                    handleClassifyUpload(document.getElementById('classify-image'));
                }
            }
        });
    });
    
    // Check backend health on page load
    checkBackendHealth();
});

// Check if backend is running
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const result = await response.json();
        
        if (response.ok) {
            console.log('✅ Backend is running:', result);
            showStatus(`✅ Backend connected (${result.device})`, 'success');
        } else {
            showStatus('⚠️ Backend responded with error', 'error');
        }
    } catch (error) {
        console.error('❌ Backend connection failed:', error);
        showStatus('❌ Backend not connected. Please start the backend server.', 'error');
    }
}

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to upload references
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const activeElement = document.activeElement;
        
        // If in generation caption field, generate image
        if (activeElement && activeElement.id === 'generation-caption') {
            generateImage();
        }
        // Otherwise, upload references if all fields are filled
        else {
            uploadReferences();
        }
    }
});