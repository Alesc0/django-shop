let error = true;

db = db.getSiblingDB("dbproj");

let res = [
  db.createCollection("users"),
  db.createCollection("products"),
  db.products.insertOne({
    _id: 1,
    name: "Product 1",
    description:
      "Vivamus suscipit tortor eget felis porttitor volutpat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur aliquet quam id dui posuere blandit. Pellentesque in ipsum id orci porta dapibus. Praesent sapien massa, convallis a pellentesque nec, egestas non nisi. Vivamus suscipit tortor eget felis porttitor volutpat. Nulla porttitor accumsan tincidunt. Vivamus magna justo, lacinia eget consectetur sed, convallis at tellus. Curabitur arcu erat, accumsan id imperdiet et, porttitor at sem. Vivamus magna justo, lacinia eget consectetur sed, convallis at tellus.",
    image: "94e2a485-b5c9-4d46-a590-b724ff192dbe",
  }),
  db.products.insertOne({
    _id: 2,
    name: "Product 2",
    description:
      "Pellentesque in ipsum id orci porta dapibus. Vestibulum ac diam sit amet quam vehicula elementum sed sit amet dui. Cras ultricies ligula sed magna dictum porta. Donec rutrum congue leo eget malesuada. Nulla quis lorem ut libero malesuada feugiat. Vestibulum ac diam sit amet quam vehicula elementum sed sit amet dui. Curabitur arcu erat, accumsan id imperdiet et, porttitor at sem. Curabitur non nulla sit amet nisl tempus convallis quis ac lectus. Curabitur aliquet quam id dui posuere blandit. Curabitur non nulla sit amet nisl tempus convallis quis ac lectus.",
    image: "d7aae002-3dbe-4017-b310-19817e751bae",
  }),
  db.users.insertOne({
    _id: 1,
    type: 1,
  }),
  db.users.insertOne({
    _id: 2,
    type: 1,
  }),
  db.users.insertOne({
    _id: 3,
    type: 3,
    company: "Company 1",
  }),
  db.users.insertOne({
    _id: 4,
    type: 2,
  }),
  db.users.insertOne({
    _id: 5,
    type: 1,
  }),
  db.users.insertOne({
    _id: 6,
    type: 3,
    company: "Pending Company Partner",
  }),
  db.users.insertOne({
    _id: 7,
    type: 1,
  }),
];

printjson(res);

if (error) {
  print("Error, exiting");
  quit(1);
}
