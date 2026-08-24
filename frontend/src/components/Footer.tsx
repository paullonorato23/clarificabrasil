import Link from "next/link";

export default function Footer() {
  return (
    <footer className="mt-16 border-t border-slate-200 bg-white">
      <div className="mx-auto max-w-6xl px-4 py-8">
        <p className="rounded-md bg-amber-50 px-4 py-3 text-sm text-amber-800">
          ⚠️ Projeto em desenvolvimento: todos os dados exibidos nesta versão são
          fictícios e servem apenas para demonstração das funcionalidades.
        </p>
        <div className="mt-6 flex flex-wrap items-center justify-between gap-4 text-sm text-slate-600">
          <p>
            <strong className="text-slate-900">Política Transparente</strong> — código
            aberto sob licença MIT, sem fins lucrativos e apartidário.
          </p>
          <nav className="flex gap-4">
            <Link href="/metodologia" className="hover:text-emerald-700">
              Metodologia
            </Link>
            <Link href="/sobre" className="hover:text-emerald-700">
              Sobre
            </Link>
            <a
              href="https://github.com/paullonorato23/politica-transparente"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-emerald-700"
            >
              GitHub
            </a>
          </nav>
        </div>
        <p className="mt-4 text-xs text-slate-400">
          Democracia se fortalece com transparência.
        </p>
      </div>
    </footer>
  );
}
