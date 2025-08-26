type Props = {
  meta?: { page: number; page_size: number; total: number };
  onPage: (p: number) => void;
};

export default function Pagination({ meta, onPage }: Props) {
  if (!meta) return null;
  const { page, page_size, total } = meta;
  const totalPages = Math.max(1, Math.ceil(total / page_size));
  return (
    <div className="mt-4 flex items-center gap-3">
      <button
        disabled={page <= 1}
        onClick={() => onPage(page - 1)}
        className="btn btn-ghost disabled:opacity-40"
      >
        Anterior
      </button>
      <span className="text-sm text-gray-600">
        Página {page} de {totalPages}
      </span>
      <button
        disabled={page >= totalPages}
        onClick={() => onPage(page + 1)}
        className="btn btn-ghost disabled:opacity-40"
      >
        Siguiente
      </button>
    </div>
  );
}
