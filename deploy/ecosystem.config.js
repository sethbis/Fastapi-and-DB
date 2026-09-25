module.exports = {
  apps: [
    {
      name: "fastapi-app",
      script: "venv/bin/uvicorn",
      args: "main:app --host 0.0.0.0 --port 8000",
      cwd: "/home/ubuntu/fastapi-aws-rds",
      interpreter: "none",
      autorestart: true,
      watch: false
    }
  ]
};
