import { NextResponse } from "next/server";
import prisma from "@/lib/prisma";

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get("q");
  const workspaceId = searchParams.get("workspaceId");

  if (!query || query.trim().length < 2) return NextResponse.json({ results: [] });
  if (!workspaceId) return NextResponse.json({ error: "workspaceId required" }, { status: 400 });

  try {
    const results = await prisma.page.findMany({
      where: {
        workspaceId,
        isDeleted: false,
        title: { contains: query.trim(), mode: "insensitive" },
      },
      select: { id: true, title: true, icon: true, parentId: true, updatedAt: true },
      orderBy: { updatedAt: "desc" },
      take: 10,
    });
    return NextResponse.json({
      results: results.map((p) => ({ ...p, updatedAt: p.updatedAt.toISOString() })),
    });
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: "Search failed" }, { status: 500 });
  }
}
