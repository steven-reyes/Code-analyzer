# src/ui/setup_prompt.py

def ask_hosting_method():
    choice = input("Will this project be hosted on localhost or deployed to another environment? (localhost/other): ")
    if choice.lower() == "localhost":
        print("Verifying localhost setup...")
        # ...
        print("Localhost documentation is complete. Adjusting configs for local usage.")
    else:
        print("Evaluating deployment readiness (CI/CD pipelines, scalability, reliability)...")
        # ...
        print("Configurations updated for cloud/server deployment.")
