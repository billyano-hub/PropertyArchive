
# PropertyArchive (Flask Version)

PropertyArchive is a web application built using **Flask**, a lightweight Python web framework.
It facilitates property listings and interactions between real estate agents and users. Whether you're looking to buy, rent, or book short-term accommodations, PropertyArchive streamlines the process.
Agents can post properties, and users can express interest in various ways.

## Features

1. **Property Listings**:
   - Agents can create detailed listings for properties, including land, houses, apartments, and short-term rentals.
   - Each listing includes essential information such as location, price, property type, and amenities.

2. **User Interaction**:
   - Users can browse through available properties, filtering by location, price range, and property type.
   - Express interest by:
     - **Buying**: Users can request more information about purchasing a property.
     - **Renting**: Users can inquire about rental availability.
     - **Booking Shortlets**: For short-term stays, users can check availability and book directly.

3. **Agent Dashboard**:
   - Agents have a personalized dashboard where they can manage their listings.
   - Features include adding new properties, updating existing listings, and responding to user inquiries.

4. **User Profiles**:
   - Users can create profiles, save favorite properties, and track their interactions with agents.
   - Agents can view user profiles to understand preferences and tailor their responses.

## Getting Started

1. **Installation**:
   - Clone this repository to your local machine.
   - Install the necessary dependencies using `pip install -r requirements.txt`.

2. **Database Setup**:
   - Set up your preferred database (e.g., SQLite, MySQL, PostgreSQL).
   - Configure the database connection in the Flask app.

3. **Environment Variables**:
   - Create a `.env` file based on the provided `.env.example`.
   - Set environment variables such as database credentials and secret keys.

4. **Run the Application**:
   - Execute `flask run` to launch the server.
   - Visit `http://localhost:5000` in your browser.

5. **Agent Registration**:
   - Agents can sign up through the application.
   - Once registered, they gain access to the agent dashboard.

## Technologies Used

- **Flask**: Backend server
- **Jinja2**: Templating engine for rendering HTML
- **SQLAlchemy**: Database management
- **WTForms**: Form handling and validation
- **Bootstrap**: Frontend styling

## Contributing

We welcome contributions! Feel free to submit pull requests or report issues.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Thank you for choosing PropertyArchive (Flask Version)! We hope it simplifies your property search and interactions. 🏠🌟
