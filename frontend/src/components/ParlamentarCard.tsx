import Link from "next/link";
import type { Parlamentar } from "@/lib/types";
import { calcularScore, resumoPromessas } from "@/lib/score";
import { rotuloCasa } from "@/lib/format";
import Avatar from "./Avatar";
import ScoreBadge from "./ScoreBadge";

export default function ParlamentarCard({ parlamentar }: { parlamentar: Parlamentar }) {
  const score = calcularScore(parlamentar.promessas, parlamentar.votacoes);
  const resumo = resumoPromessas(parlamentar.promessas);

  return (
    <Link
      href={`/parlamentares/${parlamentar.id}`}
      className="flex min-h-24 items-center gap-4 rounded-xl border border-neutral-200 bg-white p-4 shadow-sm transition hover:border-primary-300 hover:shadow-md"
    >
      <Avatar nome={parlamentar.nome} percentual={score} />
      <div className="min-w-0 flex-1">
        <p className="truncate font-semibold text-neutral-900">{parlamentar.nome}</p>
        <p className="text-sm text-neutral-600">
          {rotuloCasa(parlamentar.casa)} · {parlamentar.partido}/{parlamentar.uf}
        </p>
        <p className="mt-1 text-xs text-neutral-500">
          {resumo.cumprida}/{parlamentar.promessas.length} promessas cumpridas
        </p>
      </div>
      <ScoreBadge score={score} />
    </Link>
  );
}
