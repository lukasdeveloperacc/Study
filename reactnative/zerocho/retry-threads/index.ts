import "expo-router/entry";

import { faker } from "@faker-js/faker";
import {
  belongsTo,
  createServer,
  Factory,
  hasMany,
  Model,
  Response,
  RestSerializer,
  Server,
} from "miragejs";
import { type User } from "./app/_layout";

declare global {
  interface Window {
    server: Server;
  }
}

let zerocho: User;

if (__DEV__) {
  if (window.server) {
    window.server.shutdown();
  }

  window.server = createServer({
    models: { // database의 관계정의
      user: Model.extend({ // user : model name
        posts: hasMany("post"),
        activities: hasMany("activity"),
      }),
      post: Model.extend({
        // 게시글은 user model에 속해있음 
        // 맨 앞의 user는 attribute, 뒤의 "user"는 user model name
        user: belongsTo("user"), 
      }),
      activity: Model.extend({
        user: belongsTo("user"),
      }),
    },
    serializers: {
      // post 찾을 때마다 알아서 user를 넣어줌
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
      // 임의의 user, post를 찍어낸다.
      // faker : random 값 제조 라이브러리
      user: Factory.extend({
        id: () => faker.person.firstName(), // function으로 등록 안해놓으면 계속 같은 값이므로 주의
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
    seeds(server) { // seed : dummy data 미리 넣어놓는 기능
      // server.loadFixure() 를 이용해서 사용한 데이터를 계속 사용할 수도 있다.
      // - https://miragejs.com/docs/main-concepts/fixtures/#gatsby-focus-wrapper
      zerocho = server.create("user", {
        id: "zerohch0",
        name: "ZeroCho",
        description: "🐢 lover, programmer, youtuber",
        profileImageUrl: "https://avatars.githubusercontent.com/u/885857?v=4",
      });
      const users = server.createList("user", 10); // user 10명을 만듦
      users.forEach((user) => { // user별 post를 5개씩 만듦
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
            user: schema.find("user", "zerohch0"), // key : post에서 user attribute
          });
        });
        return new Response(200, {}, { posts });
      });

      this.get("/posts", (schema, request) => {
        console.log("user.all", schema.all("user").models);
        const cursor = parseInt((request.queryParams.cursor as string) || "0");
        const posts = schema.all("post").models.slice(cursor, cursor + 10);
        return new Response(200, {}, { posts });
      });

      this.get("/posts/:id", (schema, request) => {
        const post = schema.find("post", request.params.id);
        const comments = schema.all("post").models.slice(0, 10);
        return new Response(200, {}, { post, comments });
      });

      this.post("/login", (schema, request) => {
        const { username, password } = JSON.parse(request.requestBody);

        if (username === "zerocho" && password === "1234") {
          return {
            accessToken: "access-token",
            refreshToken: "refresh-token",
            user: {
              id: "zerohch0",
              name: "ZeroCho",
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
