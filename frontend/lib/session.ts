import { cookies } from "next/headers";
import { SignJWT, jwtVerify } from "jose";

export const COOKIE_NAME = "admin_session";
const SESSION_EXPIRATION = "8h";
const SESSION_MAX_AGE_SECONDS = 8 * 60 * 60; // 8 hours in seconds

function getSecretKey(): Uint8Array {
  const secret = process.env.SESSION_SECRET;
  if (!secret || secret.length < 32) {
    throw new Error("SESSION_SECRET must be set and at least 32 characters long.");
  }
  return new TextEncoder().encode(secret);
}

/**
 * Creates a signed JWT session cookie valid for 8 hours with secure defaults.
 */
export async function createSession(): Promise<string> {
  const secretKey = getSecretKey();

  const jwt = await new SignJWT({ role: "admin" })
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime(SESSION_EXPIRATION)
    .sign(secretKey);

  const cookieStore = await cookies();
  cookieStore.set(COOKIE_NAME, jwt, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    path: "/",
    maxAge: SESSION_MAX_AGE_SECONDS,
  });

  return jwt;
}

/**
 * Reads the session cookie and verifies its JWT signature and expiration.
 * Accepts an optional token string (useful for middleware where request.cookies is used).
 * Returns true if valid, false otherwise.
 */
export async function verifySession(token?: string): Promise<boolean> {
  try {
    let sessionToken = token;

    if (!sessionToken) {
      const cookieStore = await cookies();
      sessionToken = cookieStore.get(COOKIE_NAME)?.value;
    }

    if (!sessionToken) {
      return false;
    }

    const secretKey = getSecretKey();
    await jwtVerify(sessionToken, secretKey, {
      algorithms: ["HS256"],
    });

    return true;
  } catch {
    return false;
  }
}
