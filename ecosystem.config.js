const path = require('path');

module.exports = {
  apps: [
    {
      name: 'rag-api-dev',
      script: 'uvicorn',
      args: 'app.main:app --host 0.0.0.0 --port 8001 --log-level info',
      // Working directory - adjust if running from different location
      cwd: path.resolve(__dirname),
      // Python interpreter from virtual environment - adjust path as needed
      interpreter: path.resolve(__dirname, '..', 'mcp_env', 'bin', 'python'),
      instances: 1,
      exec_mode: 'fork',
      autorestart: true,
      watch: false,
      max_memory_restart: '2G',
      env: {
        NODE_ENV: 'production',
        PYTHONUNBUFFERED: '1',
      },
      // Log files will be created in logs/ directory relative to cwd
      error_file: './logs/rag-api-error.log',
      out_file: './logs/rag-api-out.log',
      log_file: './logs/rag-api-combined.log',
      time: true,
      merge_logs: true,
      kill_timeout: 5000,
      wait_ready: true,
      listen_timeout: 10000,
    },
  ],
};

