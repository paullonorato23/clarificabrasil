"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const LINKS = [
  { href: "/", rotulo: "Início" },
  { href: "/parlamentares", rotulo: "Parlamentares" },
  { href: "/comparar", rotulo: "Comparar" },
  { href: "/moderacao", rotulo: "Moderação" },
  { href: "/metodologia", rotulo: "Metodologia" },
  { href: "/sobre", rotulo: "Sobre" },
];

function estaAtivo(pathname: string, href: string): boolean {
  if (href === "/") return pathname === "/";
  return pathname.startsWith(href);
}

export default function Header() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-10 border-b border-neutral-200 bg-white/95 backdrop-blur">
      <div className="mx-auto flex max-w-6xl flex-wrap items-center gap-x-6 gap-y-2 px-4 py-3">
        <Link href="/" className="flex min-h-11 items-center gap-2 text-lg font-bold text-neutral-900">
          <span className="flex h-9 w-9 items-center justify-center rounded-md bg-primary-700 text-sm font-extrabold text-white">
            PT
          </span>
          <span>
            Política <span className="text-primary-700">Transparente</span>
          </span>
        </Link>
        <nav aria-label="Navegação principal" className="ml-auto flex max-w-full gap-1 overflow-x-auto text-sm font-medium">
          {LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={`rounded-md px-3 py-2 whitespace-nowrap ${
                estaAtivo(pathname, link.href)
                  ? "bg-primary-100 text-primary-800"
                  : "text-neutral-600 hover:bg-neutral-100 hover:text-neutral-900"
              }`}
            >
              {link.rotulo}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
