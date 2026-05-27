
module.exports = {
  apps: [{
    name: "smolgo-server",
    script: "venv/bin/uvicorn",
    args: "app.main:app --host 127.0.0.1 --port 8001",
    cwd: "/root/SmolGo_Server",
    interpreter: "python3",
    exec_mode: "fork",
    
    env: {
      "PATH": "/root/SmolGo_Server/venv/bin:$PATH"
    },
    env_production: {
      "NODE_ENV": "production"
    }
  }]
}