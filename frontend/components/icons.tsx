import type { ReactNode, SVGProps } from "react";

export type IconName =
  | "scale"
  | "arrow"
  | "shield"
  | "document"
  | "message"
  | "upload"
  | "search"
  | "check"
  | "clock"
  | "book"
  | "plus"
  | "external";

export function Icon({
  name,
  size = 20,
  ...props
}: SVGProps<SVGSVGElement> & { name: IconName; size?: number }) {
  const common = {
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 1.9,
    strokeLinecap: "round" as const,
    strokeLinejoin: "round" as const,
    "aria-hidden": true
  };

  const paths: Record<IconName, ReactNode> = {
    scale: (
      <>
        <path d="M12 3v18M5 6h14M7.5 6 4 13h7L7.5 6ZM16.5 6 13 13h7l-3.5-7ZM8 21h8" />
        <path d="M4 13c.4 2 1.6 3 3.5 3S10.6 15 11 13M13 13c.4 2 1.6 3 3.5 3S19.6 15 20 13" />
      </>
    ),
    arrow: <path d="M5 12h13M14 7l5 5-5 5" />,
    shield: (
      <>
        <path d="M12 3 5 6v5c0 4.8 2.8 8.4 7 10 4.2-1.6 7-5.2 7-10V6l-7-3Z" />
        <path d="m9.3 12 1.8 1.8 3.8-4" />
      </>
    ),
    document: (
      <>
        <path d="M7 3h7l4 4v14H7z" />
        <path d="M14 3v5h5M10 12h5M10 16h5" />
      </>
    ),
    message: (
      <>
        <path d="M4 5h16v11H9l-5 4V5Z" />
        <path d="M8 9h8M8 12h6" />
      </>
    ),
    upload: (
      <>
        <path d="M12 16V5M8 9l4-4 4 4" />
        <path d="M5 14v5h14v-5" />
      </>
    ),
    search: (
      <>
        <circle cx="11" cy="11" r="6.5" />
        <path d="m16 16 4 4" />
      </>
    ),
    check: <path d="m5 12 4 4L19 6" />,
    clock: (
      <>
        <circle cx="12" cy="12" r="8" />
        <path d="M12 8v5l3 2" />
      </>
    ),
    book: (
      <>
        <path d="M4 5.5A3.5 3.5 0 0 1 7.5 2H11v17H7.5A3.5 3.5 0 0 0 4 22V5.5Z" />
        <path d="M20 5.5A3.5 3.5 0 0 0 16.5 2H13v17h3.5A3.5 3.5 0 0 1 20 22V5.5Z" />
      </>
    ),
    plus: <path d="M12 5v14M5 12h14" />,
    external: (
      <>
        <path d="M14 5h5v5M13 11l6-6" />
        <path d="M18 13v6H5V6h6" />
      </>
    )
  };

  return (
    <svg {...common} {...props}>
      {paths[name]}
    </svg>
  );
}
