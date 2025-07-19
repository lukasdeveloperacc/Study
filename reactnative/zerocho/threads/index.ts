import "expo-router/entry";

import {
  belongsTo,
  createServer,
  hasMany,
  Model,
  Response,
  RestSerializer,
  Server,
  Factory,
} from "miragejs";
import { faker } from "@faker-js/faker";
import { type User } from "./app/_layout";

declare global {
  interface Window {
    server: Server;
  }
}

let lotto;

if (__DEV__) {
  if (window.server) {
    window.server.shutdown();
  }

  window.server = createServer({
    models: {
      user: Model.extend({
        posts: hasMany("post"),
        activities: hasMany("activity"),
      }),
      post: Model.extend({
        user: belongsTo("user"),
      }),
      activity: Model.extend({
        user: belongsTo("user"),
      }),
    },
    serializers: {
      post: RestSerializer.extend({
        include: ["user"],
        embed: true,
      }),
      activity: RestSerializer.extend({
        include: ["user"],
        embed: true,
      }),
    },
    factories: {
      user: Factory.extend({
        id: () => faker.person.firstName(),
        name: () => faker.person.fullName(),
        description: () => faker.lorem.sentence(),
        profileImageUrl: () =>
          `https://avatars.githubusercontent.com/u/${Math.floor(
            Math.random() * 100_000
          )}?v=4`,
        isVerified: () => Math.random() > 0.5,
      }),
      post: Factory.extend({
        id: () => faker.string.numeric(6),
        content: () => faker.lorem.paragraph(),
        imageUrls: () =>
          Array.from({ length: Math.floor(Math.random() * 3) }, () =>
            faker.image.urlLoremFlickr()
          ),
        likes: () => Math.floor(Math.random() * 100),
        comments: () => Math.floor(Math.random() * 100),
        reposts: () => Math.floor(Math.random() * 100),
      }),
    },
    seeds(server) {
      lotto = server.create("user", {
        id: "lotto0",
        name: "Lotto",
        description: "🐢 lover, programmer, youtuber",
        profileImageUrl: "https://avatars.githubusercontent.com/u/885857?v=4",
      });
      const users = server.createList("user", 10);
      users.forEach((user) => {
        server.createList("post", 5, {
          user,
        });
      });
    },
    routes() {
      this.post("/posts", (schema, request) => {
        const { posts } = JSON.parse(request.requestBody);
        posts.forEach((post: any) => {
          schema.create("post", {
            content: post.content,
            imageUrls: post.imageUrls,
            location: post.location,
            user: schema.find("user", "lotto0"),
          });
        });
        return new Response(200, {}, { posts });
      });

      this.get("/posts", (schema, request) => {
        let posts = schema.all("post");
        if (request.queryParams.type === "following") {
          posts = posts.filter((post) => post.user?.id === lotto?.id);
        }

        let targetIndex = -1;
        if (request.queryParams.cursor) {
          targetIndex = posts.models.findIndex((v) => v.id === request.queryParams.cursor)
        } 
        return posts.slice(targetIndex + 1, targetIndex + 11);
      });

      this.get("/posts/:id", (schema, request) => {
        const post = schema.find("post", request.params.id);
        return schema.all("post").slice(0, 10);
      });

      this.post("/login", (schema, request) => {
        const { username, password } = JSON.parse(request.requestBody);

        if (username === "lotto" && password === "1234") {
          return {
            accessToken: "access-token",
            refreshToken: "refresh-token",
            user: {
              id: "lotto0",
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
