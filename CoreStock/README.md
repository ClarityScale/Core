# Global Event-Driven Market Intelligence Analyst

This project is a React application designed for performing market impact assessments and generating structured investment opportunity tables based on user-provided events. 

## Features

- **Event Input**: Users can input details about market events for analysis.
- **Impact Assessment**: The application analyzes the market impact of the provided events.
- **Investment Opportunities**: Generates a structured table of investment opportunities based on the analysis results.
- **Dashboard**: A main page to display analysis results and opportunities.
- **Settings**: Allows users to configure application preferences.

## Project Structure

```
global-event-driven-market-intel
├── public
│   └── index.html          # Main HTML document
├── src
│   ├── index.tsx          # Entry point for the React application
│   ├── App.tsx            # Main App component
│   ├── main.css           # Global styles
│   ├── components          # Reusable components
│   │   ├── Header.tsx
│   │   ├── EventForm.tsx
│   │   ├── ImpactAssessment.tsx
│   │   ├── OpportunityTable.tsx
│   │   └── Footer.tsx
│   ├── pages               # Application pages
│   │   ├── Dashboard.tsx
│   │   └── Settings.tsx
│   ├── hooks               # Custom hooks
│   │   └── useAssessments.ts
│   ├── services            # API and assessment logic
│   │   ├── api.ts
│   │   └── assessmentEngine.ts
│   ├── utils               # Utility functions
│   │   └── formatter.ts
│   ├── types               # TypeScript types and interfaces
│   │   └── index.ts
│   └── assets              # Asset files
│       └── fonts
├── package.json            # NPM configuration
├── tsconfig.json           # TypeScript configuration
├── vite.config.ts          # Vite configuration
├── .gitignore              # Git ignore file
└── README.md               # Project documentation
```

## Getting Started

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd global-event-driven-market-intel
   ```

2. **Install dependencies**:
   ```
   npm install
   ```

3. **Run the application**:
   ```
   npm run dev
   ```

4. **Open your browser** and navigate to `http://localhost:3000` to view the application.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

## License

This project is licensed under the MIT License.