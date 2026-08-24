import type { Metadata } from "next";
import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: {
    default: "Política Transparente",
    template: "%s — Política Transparente",
  },
  description:
    "O que seu representante prometeu vs. o que ele realmente fez? Plataforma colaborativa e sem fins lucrativos para monitorar deputados e senadores com dados oficiais.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="pt-BR">
      <body className="flex min-h-screen flex-col">
        <Header />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
