const uploadBtn = document.getElementById('resume-upload');
const atsBtn = document.getElementById('ats-btn');
const structureBtn = document.getElementById('structure-btn');
const jobMatchBtn = document.getElementById('job-match-btn');
const jobDescriptionInput = document.getElementById('job-description');

// Backend URL
const API_URL = 'http://localhost:8000';

let requestId = null;

const loader = document.getElementById('loader');

uploadBtn.addEventListener('change', async (event) => {
    const formData = new FormData();
    formData.append('file', event.target.files[0]);

    // Show the loader while uploading the file
    showLoader();

    try {
        const response = await fetch('${API_URL}/upload', {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        requestId = data.request_id;
        alert('Resume uploaded successfully!');
    } catch (error) {
        console.error('Error uploading file:', error);
    } finally {
        // Hide the loader once the API call is complete
        hideLoader();
    }
});

atsBtn.addEventListener('click', async () => {
    if (!requestId) {
        alert('Please upload a resume first!');
        return;
    }

    // Show the loader while fetching the ATS score
    showLoader();

    try {
        const response = await fetch(`${API_URL}/analyze/ats/${requestId}`);
        const data = await response.json();
        displayAtsResult(data.result);
    } catch (error) {
        console.error('Error fetching ATS score:', error);
    } finally {
        // Hide the loader once the API call is complete
        hideLoader();
    }
});

structureBtn.addEventListener('click', async () => {
    if (!requestId) {
        alert('Please upload a resume first!');
        return;
    }

    // Show the loader while fetching the structure review
    showLoader();

    try {
        const response = await fetch(`${API_URL}/analyze/resume-structure/${requestId}`);
        const data = await response.json();
        displayStructureResult(data.result);
    } catch (error) {
        console.error('Error fetching structure review:', error);
    } finally {
        // Hide the loader once the API call is complete
        hideLoader();
    }
});

jobMatchBtn.addEventListener('click', async () => {
    if (!requestId) {
        alert('Please upload a resume first!');
        return;
    }

    const jobDescription = jobDescriptionInput.value;

    // Ensure the job description is provided
    if (!jobDescription.trim()) {
        alert('Please enter a job description to get the Job Match Analysis!');
        return;
    }

    const formData = new FormData();
    formData.append('job_description', jobDescription);

    // Show the loader while fetching the job match analysis
    showLoader();

    try {
        const response = await fetch(`${API_URL}/analyze/job-match/${requestId}`, {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        displayJobMatchResult(data.result);
    } catch (error) {
        console.error('Error fetching job match:', error);
    } finally {
        // Hide the loader once the API call is complete
        hideLoader();
    }
});

// Function to display the loader
function showLoader() {
    loader.classList.remove('hidden');
}

// Function to hide the loader
function hideLoader() {
    loader.classList.add('hidden');
}

// Functions to display results
function displayAtsResult(result) {
    document.getElementById('ats-overall').innerText = result.overall;
    document.getElementById('ats-keywords').innerText = result.keywords.join(', ');
    document.getElementById('ats-missing-keywords').innerText = result.missing_keywords.join(', ');
    document.getElementById('ats-format').innerText = result.format_score;
    document.getElementById('ats-result').style.display = 'block';
}

function displayStructureResult(result) {
    document.getElementById('structure-completeness').innerText = result.completeness;
    document.getElementById('structure-sections-present').innerText = result.sections_present.join(', ');
    document.getElementById('structure-sections-missing').innerText = result.sections_missing.join(', ');
    document.getElementById('structure-suggestions').innerText = result.suggestions.join(', ');
    document.getElementById('structure-readability').innerText = result.readability;
    document.getElementById('structure-result').style.display = 'block';
}

function displayJobMatchResult(result) {
    document.getElementById('job-match-score').innerText = result.score;
    document.getElementById('job-match-skills').innerText = result.matching_skills.join(', ');
    document.getElementById('job-match-missing-skills').innerText = result.missing_skills.join(', ');
    document.getElementById('job-match-recommendations').innerText = result.recommendations.join(', ');
    document.getElementById('job-match-relevance').innerText = result.relevance;
    document.getElementById('job-match-result').style.display = 'block';
}
