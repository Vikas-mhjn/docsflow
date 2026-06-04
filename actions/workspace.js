"use server";
import prisma from "@/lib/prisma";
import { revalidatePath } from "next/cache";

export async function createWorkspace(data) {
  const { name, icon, userId } = data;
  if (!name || !name.trim()) return { error: "Workspace name is required" };
  try {
    const workspace = await prisma.workspace.create({
      data: { name: name.trim(), icon: icon || "📁", userId },
    });
    revalidatePath("/dashboard");
    return { workspace };
  } catch (error) {
    console.error(error);
    return { error: "Failed to create workspace." };
  }
}
