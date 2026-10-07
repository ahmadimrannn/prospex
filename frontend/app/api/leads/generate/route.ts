import { NextResponse } from "next/server";

export const maxDuration = 60;

export async function POST(request: Request) {
  try {
    const body = await request.json();

    const upstreamResponse = await fetch("https://prospex-green.vercel.app/leads/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
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
