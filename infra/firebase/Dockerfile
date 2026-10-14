# Emuladores de Firebase (Firestore, Auth, Storage) + Emulator UI
FROM node:20-slim

# Java es necesario para los emuladores de Firestore y Storage.
RUN apt-get update && apt-get install -y --no-install-recommends \
        default-jre-headless \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g firebase-tools@13

WORKDIR /firebase

EXPOSE 4000 8080 9099 9199

CMD ["firebase", "emulators:start", "--project", "acralis-dev"]
