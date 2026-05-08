require("dotenv").config();

const nodemailer = require("nodemailer");
const path = require("path");

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

    // Email content
    const jobDetails = jobRecommendations.map(job => `\nRole: ${job.jobRole}\nCompany: ${job.companyName}\nLink: ${job.jobLink}`).join("\n");

    const mailOptions = {
      from: process.env.EMAIL_USER,
      to: userEmail,
      subject: `New Job Matches Found`,
      text: `\nHi ${userName},\n\nWe found some job matches for you! 🎯\n\n${jobDetails}\n\nGood luck 🚀\n\n- Your AI Job Assistant`,
    };

    // Send email
    const info = await transporter.sendMail(mailOptions);

    console.log("✅ Email sent!");
    console.log(info.response);
  } catch (error) {
    console.error("❌ Error:");
    console.error(error);
  }
}

// Example trigger
sendJobRecommendationEmail({
  userEmail: "user@gmail.com",
  userName: "User Name",
  jobRecommendations: [
    { jobRole: "Backend Developer Intern", companyName: "Company 1", jobLink: "https://example.com/job1" },
    { jobRole: "Frontend Developer", companyName: "Company 2", jobLink: "https://example.com/job2" },
    { jobRole: "Full Stack Developer", companyName: "Company 3", jobLink: "https://example.com/job3" },
    { jobRole: "DevOps Engineer", companyName: "Company 4", jobLink: "https://example.com/job4" },
    { jobRole: "Data Scientist", companyName: "Company 5", jobLink: "https://example.com/job5" },
  ],
});