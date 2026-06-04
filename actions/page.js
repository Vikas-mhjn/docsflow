"use server";
import prisma from "@/lib/prisma";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

export async function createPage(workspaceId, parentId = null) {
  const page = await prisma.page.create({
    data: { title: "Untitled", workspaceId, parentId },
  });
  revalidatePath("/workspace/" + workspaceId);
  redirect("/workspace/" + workspaceId + "/" + page.id);
}

export async function updatePage(pageId, data) {
  try {
    await prisma.page.update({ where: { id: pageId }, data });
    return { success: true };
  } catch (e) {
    return { error: "Failed to save." };
  }
}

export async function toggleFavorite(pageId, workspaceId) {
  const page = await prisma.page.findUnique({ where: { id: pageId }, select: { isFavorited: true } });
  if (!page) return { error: "Page not found" };
  const updated = await prisma.page.update({ where: { id: pageId }, data: { isFavorited: !page.isFavorited } });
  revalidatePath("/workspace/" + workspaceId);
  return { isFavorited: updated.isFavorited };
}

async function softDeleteRecursive(pageId) {
  const children = await prisma.page.findMany({ where: { parentId: pageId }, select: { id: true } });
  for (const c of children) await softDeleteRecursive(c.id);
  await prisma.page.update({ where: { id: pageId }, data: { isDeleted: true } });
}

export async function deletePage(pageId, workspaceId) {
  await softDeleteRecursive(pageId);
  revalidatePath("/workspace/" + workspaceId);
  redirect("/workspace/" + workspaceId);
}

export async function restorePage(pageId, workspaceId) {
  await prisma.page.update({ where: { id: pageId }, data: { isDeleted: false } });
  revalidatePath("/workspace/" + workspaceId);
  return { success: true };
}

export async function permanentlyDeletePage(pageId, workspaceId) {
  await prisma.page.delete({ where: { id: pageId } });
  revalidatePath("/workspace/" + workspaceId);
  return { success: true };
}
