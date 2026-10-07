import { NextResponse } from "next/server";
import crypto from "crypto";
import { createSession } from "@/lib/session";

/**
 * Safely compares two strings using crypto.timingSafeEqual on equal-length SHA-256 digests.
 * This guarantees buffers are always equal length (32 bytes) preventing errors and timing attacks.
 */
function safeCompare(input: string, expected: string): boolean {
  const hashInput = crypto.createHash("sha256").update(input).digest();
  const hashExpected = crypto.createHash("sha256").update(expected).digest();
  return crypto.timingSafeEqual(hashInput, hashExpected);
}

export async function POST(request: Request) {
  try {
    const body = await request.json().catch(() => ({}));
    const username = typeof body.username === "string" ? body.username : "";
    const password = typeof body.password === "string" ? body.password : "";

    const envUser = process.env.ADMIN_USERNAME!;
    const envPass = process.env.ADMIN_PASSWORD!;

    const isUserValid = envUser.length > 0 && safeCompare(username, envUser);
    const isPassValid = envPass.length > 0 && safeCompare(password, envPass);

    if (!isUserValid || !isPassValid) {
      // Small delay (~500ms) on failure to mitigate brute-force attempts
      await new Promise((resolve) => setTimeout(resolve, 500));
      return NextResponse.json(
        { message: "Invalid username or password" },
        { status: 401 }
      );
    }

    // Create session cookie with 8-hour expiration
    await createSession();

    return NextResponse.json(
      { message: "Logged in successfully" },
      { status: 200 }
    );
  } catch {
    // Artificial delay on unexpected errors before 401 response
    await new Promise((resolve) => setTimeout(resolve, 500));
    return NextResponse.json(
      { message: "Invalid username or password" },
      { status: 401 }
    );
  }
}
