import type { Metadata } from "next";
import { Inter, JetBrains_Mono, Newsreader } from "next/font/google";
import type { ReactNode } from "react";
import "./globals.css";

const newsreader = Newsreader({ subsets: ["latin"], variable: "--font-newsreader", display: "swap" });
const inter = Inter({ subsets: ["latin"], variable: "--font-inter", display: "swap" });
const jetbrainsMono = JetBrains_Mono({ subsets: ["latin"], variable: "--font-jetbrains-mono", display: "swap" });

export const metadata: Metadata = {
    title: "Compliance-Agent",
    description: "Autonomous FinTech regulatory compliance copilot (OJK, BI, UU PDP)",
};

export default function RootLayout({ children }: { children: ReactNode }) {
    return (
        <html lang="id" className={`${newsreader.variable} ${inter.variable} ${jetbrainsMono.variable}`}>
            <body className="min-h-screen antialiased">{children}</body>
        </html>
    );
}
