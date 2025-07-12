import "expo-router/entry";

import { createServer, Response, Server } from "miragejs";

declare global {
    interface Window {
        server: Server
    }
}

if (__DEV__) { // DEV means that it's only dev environment 
    if (window.server) {
        window.server.shutdown();
    }

    window.server = createServer({
        routes() {
          this.post("/login", (schema, request) => {
            console.log("Request : ", request);
            const { username, password } = JSON.parse(request.requestBody);
    
            if (username === "lotto" && password === "1234") {
              return {
                accessToken: "access-token",
                refreshToken: "refresh-token",
                user: {
                  id: "lotto",
                  name: "Lotto",
                  description: "🐢 lover, programmer, youtuber",
                  profileImageUrl:
                    "https://avatars.githubusercontent.com/u/885857?v=4",
                },
              };
            } else {
              return new Response(401, {}, { message: "Invalid credentials" });
            }
          });
        },
    });
}
