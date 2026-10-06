import type { Metadata } from "next";
import { Manrope, Geist } from "next/font/google";
import "./globals.css";

const manrope = Manrope({
  variable: "--font-manrope",
  subsets: ["latin"],
});

const geistSans = Geist({
  variable: "--font-geist",
  subsets: ["latin"],
});


export const metadata: Metadata = {
  title: "Prospex | Lead Collection Agent",
  description: "A complete lead collection system built by Ahmad.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${manrope.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
