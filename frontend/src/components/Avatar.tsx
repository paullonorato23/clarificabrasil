import { faixaDePercentual } from "@/lib/score";

const TAMANHOS = {
  sm: "h-10 w-10 text-sm",
  md: "h-14 w-14 text-lg",
  lg: "h-20 w-20 text-2xl",
} as const;

interface AvatarProps {
  nome: string;
  tamanho?: keyof typeof TAMANHOS;
  percentual: number;
}

/** Placeholder de foto: a cor das iniciais representa a entrega de promessas. */
export default function Avatar({ nome, tamanho = "md", percentual }: AvatarProps) {
  const partes = nome.split(" ").filter(Boolean);
  const iniciais = `${partes[0]?.[0] ?? ""}${partes[partes.length - 1]?.[0] ?? ""}`.toUpperCase();
  const cor = faixaDePercentual(percentual).barra;

  return (
    <span
      aria-hidden
      title={`${percentual}%`}
      className={`flex shrink-0 items-center justify-center rounded-full font-bold text-white ${cor} ${TAMANHOS[tamanho]}`}
    >
      {iniciais}
    </span>
  );
}
