let error = true;

db = db.getSiblingDB('dbproj');

let res = [
  db.createCollection("users"),
  db.createCollection("products"),
  db.products.insertOne({
    _id: 1,
    name: "test",
    description:
      "Sed porttitor lectus nibh. Cras ultricies ligula sed magna dictum porta. Mauris blandit aliquet elit, eget tincidunt nibh pulvinar a. Curabitur non nulla sit amet nisl tempus convallis quis ac lectus. Praesent sapien massa, convallis a pellentesque nec, egestas non nisi. Curabitur non nulla sit amet nisl tempus convallis quis ac lectus. Vivamus magna justo, lacinia eget consectetur sed, convallis at tellus. Cras ultricies ligula sed magna dictum porta. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec velit neque, auctor sit amet aliquam vel, ullamcorper sit amet ligula. Vestibulum ac diam sit amet quam vehicula elementum sed sit amet dui.",
    image: "69fb6c64-b45a-4f3b-a65e-ed38f24643e0",
  }),
  db.products.insertOne({
    _id: 2,
    name: "image",
    description:
      "Sed porttitor lectus nibh. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus magna justo, lacinia eget consectetur sed, convallis at tellus. Praesent sapien massa, convallis a pellentesque nec, egestas non nisi. Vivamus suscipit tortor eget felis porttitor volutpat. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec velit neque, auctor sit amet aliquam vel, ullamcorper sit amet ligula. Curabitur aliquet quam id dui posuere blandit. Sed porttitor lectus nibh. Nulla porttitor accumsan tincidunt. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec velit neque, auctor sit amet aliquam vel, ullamcorper sit amet ligula.",
    image: "1c009bd5-2679-4efc-a699-4d7b814f053a",
  }),
  db.users.insertOne({
    _id: 1,
    type: 1,
  }),
  db.users.insertOne({
    _id: 2,
    type: 2,
    company: "Alex Nation",
  }),
];

printjson(res);

if (error) {
  print("Error, exiting");
  quit(1);
}
