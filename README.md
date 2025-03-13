# TaskFlowX

TaskFlowX is a lightweight and modular workflow automation engine inspired by n8n, fully written in Python. It enables seamless execution of workflows triggered by various events (webhooks, scheduled tasks, emails, etc.).

## ✨ Key Features
- 🔄 **Modular Triggers**: Webhooks, schedules, emails, and more.
- ⚙️ **Dynamic Workflows**: Define your workflows by inheriting from the `Workflow` class.
- 🛠 **Dynamic Loading**: Easily add custom triggers and workflows.
- 🔄 **Multi-threaded Execution**: Optimized handling of blocking and non-blocking tasks.
- ✅ **Advanced Logging with Rich**: Detailed workflow execution tracking.
- 💡 **Extensible and Open Source**: Add your own triggers and workflows.

## 🛠 Installation
```sh
pip install taskflowx
```

## ⚡ Usage
Run TaskFlowX with the following command:
```sh
python -m taskflowx
```

## 📝 Example Workflow
Create a file `workflows/my_workflow.py`:
```python
from taskflowx.workflows.base import Workflow, trigger

class MyWorkflow(Workflow):
    @trigger("webhook")
    def handle_webhook(self, data):
        print(f"Received data via Webhook: {data}")

    @trigger("schedule")
    def run_scheduled_task(self):
        print("Scheduled task executed at regular intervals")
```

## 💪 Contributing
Contributions are welcome! Fork the repo and submit your improvements.

## 🌍 License
TaskFlowX is licensed under the MIT License.

