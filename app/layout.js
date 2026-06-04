import "./globals.css";

export const metadata = {
  title: "DocsFlow",
  description: "Modern documentation and workspace platform",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
