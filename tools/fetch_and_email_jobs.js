require("dotenv").config();

const nodemailer = require("nodemailer");

// ---------------- ENV VARIABLES ----------------
const ADZUNA_APP_ID = process.env.ADZUNA_APP_ID;
const ADZUNA_APP_KEY = process.env.ADZUNA_APP_KEY;

// ---------------- FETCH JOBS ----------------
async function fetchJobs(keyword, country) {
    try {
        const url = `https://api.adzuna.com/v1/api/jobs/${country}/search/1?app_id=${ADZUNA_APP_ID}&app_key=${ADZUNA_APP_KEY}&what=${encodeURIComponent(
            keyword
        )}&results_per_page=5`;

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`Adzuna API Error: ${response.status}`);
        }

        const data = await response.json();

        return data.results || [];
    } catch (error) {
        console.error("❌ Failed to fetch jobs:");
        console.error(error.message);
        return [];
    }
}

// ---------------- SEND EMAIL ----------------
async function sendJobRecommendationEmail({
    userEmail,
    userName,
    jobRecommendations,
}) {
    try {
        // Create transporter
        const transporter = nodemailer.createTransport({
            service: "gmail",
            auth: {
                user: process.env.EMAIL_USER,
                pass: process.env.EMAIL_PASS,
            },
        });

        // Format jobs
        const jobDetails = jobRecommendations
            .map(
                (job, index) => `
${index + 1}. ${job.title}

Company : ${job.company.display_name}
Location: ${job.location.display_name}
Apply   : ${job.redirect_url}
`
            )
            .join("\n----------------------------------------\n");

        // Email options
        const mailOptions = {
            from: process.env.EMAIL_USER,
            to: userEmail,
            subject: "🚀 New Job Matches Found",
            text: `
Hi ${userName},

We found some job matches for you 🎯

${jobDetails}

Good luck 🚀

- Your AI Job Assistant
`,
        };

        // Send email
        const info = await transporter.sendMail(mailOptions);

        console.log("\n✅ Email sent successfully!");
        console.log(info.response);

    } catch (error) {
        console.error("❌ Failed to send email:");
        console.error(error.message);
    }
}

// ---------------- MAIN ----------------
(async function () {

    // Get email from command line
    const userEmail = process.argv[2];

    // Optional job keyword
    const keyword = process.argv[3] || "developer";

    // Validate email
    if (!userEmail) {
        console.log("❌ Please provide an email address\n");

        console.log("Usage:");
        console.log("node fetch_and_email_jobs.js email@gmail.com");
        console.log("node fetch_and_email_jobs.js email@gmail.com python");

        process.exit(1);
    }

    console.log(`\n🔍 Fetching "${keyword}" jobs...\n`);

    // Fetch jobs
    const jobs = await fetchJobs(keyword, "in");

    if (jobs.length === 0) {
        console.log("❌ No jobs found.");
        return;
    }

    console.log(`✅ Found ${jobs.length} jobs\n`);

    // Send email
    await sendJobRecommendationEmail({
        userEmail,
        userName: "Calvin",
        jobRecommendations: jobs,
    });

})();
