# natsops
A full development CI/CD pipeline environment for building NATS cluster development


Nexus Configuration:

1. Navigate to http://localhost:8081/.
2. Sign in with default administrator account:
	Username: administrator
	Password: <See /volumes/nexus-data/admin.password>
3. Change existing admin password.
4. Choose "Disable anonymous access". (TBD)

Create Your User Account.

1. Go to Setting -> Security -> Users.
2. Click "Create local user."
3. Create "testuser" with appropriate information 
4. Set "Status" to "Active".
5. Set "Roles" to be "nx-admin".
6. Click "Create local user".

Setting up Blob Stores to store images from Docker Hub.

1. Go to Setting (gear icon) -> Blob Stores. Click on "Create Blob Store".
2. For type, select "File".
3. For name, select "docker-hub" and click "save".

Setting up Security Realms for Docker Hub.

1. Go to Setting -> Security -> Realms.
2. Add "Docker Bearer Token Realm" and save. (This allows anonymous pull from Nexus)

Setting up Repositories.

1. Go to Setting -> Repository -> Repositories.
2. Click on "Create repository" and select "docker (proxy)".
3. For name, type "docker-hub".
4. For HTTP, type "8082".
5. Check for "Allow anonymous docker pull".
6. For Proxy -> Remote storage, type "https://registry-1.docker.io".
7. For Docker Index, select "Use Docker Hub".
8. For Storage -> Blob Store, select "docker-hub". Click "Create Repository".
9. You should see "docker-hub" repository created.
10. You should be able to do "docker pull localhost:8082/<image name>", the image will be pulled from docker hub.

For Docker Desktop (Windows)

1. Under Settings -> Docker Engine, add the following code section:
  "insecure-registries": [
    "localhost:8082",
    "localhost:8083"
  ]
2. Click "Apply & Restart".

Setting up Blob Stores to store images for private registry.

1. Go to Setting (gear icon) -> Blob Stores. Click on "Create Blob Store".
2. For type, select "File".
3. For name, select "docker-private" and click "save".

Setting up Repositories.

1. Go to Setting -> Repository -> Repositories.
2. Click on "Create repository" and select "docker (hosted)".
3. For name, type "docker-private".
4. For HTTP, type "8083".
8. For Storage -> Blob Store, select "docker-private". Click "Create Repository".
9. You should see "docker-private" repository created.
10. You should be able to do "docker build -t localhost:8083/<image name> .", the image will be built with private registry tag.
11. Docker login into the privat registry "docker login localhost:8083"
  
Generate Maven Master Password:

1. Run "mvn --encrypt-master-password". Type a master-password. Copy the encrypted master password.
2. Create a "settings-security.xml" in the .m2 folder under your user home directory (Create one if it doesn't exist)
3. Copy the following into the security xml.
<settingsSecurity>
  <master>OUTPUT OF THE COMMAND: mvn --encrypt-master-password</master>
</settingsSecurity>

Generate Nexus Encrypted Password:

1. Run "mvn --encrypt-password <Nexus user password>". 
2. Copy the encrypted nexus user password into the "settings.xml" under your .m2 directory.

Grafana - Prometheus Setup:

1. Login to Grafana UI (http://localhost:3000) with admin/admin. (Change password afterward)
2. Add a Prometheus data source with the following parameters:
   a. Name: NATS-Prometheus
   b. Type: Prometheus
   c. Target URL: http://localhost:9090
3. Leave the rest as defaults.
4. Import the Grafana NATS dashboard JSON file in the UI. (observability/grafana-nats-dash.json)

Enable Kubernetes Support In Docker Desktop:

1. Under Settings -> Kubernetes, select "Enable Kubernetes" and "Show system containers (advanced)". Apply & restart docker desktop.
2. After Kubernetes is running, try executing "kubectl version". 
3. If issues arise, try switching the K8N current context to "docker-desktop".
   a. kubectl config use-context docker-desktop.
   b. Run "kubectl version" and ensure kubectl is working properly.

