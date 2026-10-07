import { NextResponse, type NextRequest } from "next/server";
import { verifySession, COOKIE_NAME } from "@/lib/session";

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const sessionToken = request.cookies.get(COOKIE_NAME)?.value;
  const isValid = await verifySession(sessionToken);

  // If a logged-in user opens /login, redirect them to /
  if (pathname === "/login") {
    if (isValid) {
      return NextResponse.redirect(new URL("/", request.url));
    }
    return NextResponse.next();
  }

  // Allow login API endpoint
  if (pathname === "/api/auth/login") {
    return NextResponse.next();
  }

  // Protected routes: redirect pages to /login, return 401 JSON for /api routes
  if (!isValid) {
    if (pathname.startsWith("/api/")) {
      return NextResponse.json(
        { detail: "Unauthorized" },
        { status: 401 }
      );
    }
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public files with common static extensions
     */
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
