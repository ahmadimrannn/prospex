import { NextResponse } from "next/server";
import { verifySession } from "@/lib/session";

export const maxDuration = 60;

export async function POST(request: Request) {
  try {
    // Defense-in-depth: verify session even if protected by middleware
    const isAuthenticated = await verifySession();
    if (!isAuthenticated) {
      return NextResponse.json(
        { detail: "Unauthorized" },
        { status: 401 }
      );
    }

    const body = await request.json();

    const upstreamResponse = await fetch("https://prospex-green.vercel.app/leads/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${process.env.API_ACCESS_TOKEN}`,
      },
      body: JSON.stringify(body),
    });

    const data = await upstreamResponse.json().catch(() => ({}));
    return NextResponse.json(data, { status: upstreamResponse.status });
  } catch (error) {
    return NextResponse.json(
      {
        message: error instanceof Error ? error.message : "Failed to connect to upstream service",
      },
      { status: 500 }
    );
  }
}
