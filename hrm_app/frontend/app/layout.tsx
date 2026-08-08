import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HRM Detective",
  description: "Attendance & payroll checker — rules + AI",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <header className="topbar">
          <div className="wrap">
            <a className="brand" href="/">
              <b>HRM Detective</b>
              <span>attendance &amp; payroll audit</span>
            </a>
            <nav className="nav">
              <a href="/">Dashboard</a>
              <a href="/chat">Chat</a>
            </nav>
          </div>
        </header>
        <main className="wrap">{children}</main>
      </body>
    </html>
  );
}
