"use client";

import * as React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

// Validation schema matching backend requirements
const leadFormSchema = z.object({
  industry: z
    .string()
    .trim()
    .min(1, "Industry is required")
    .max(200, "Industry must be at most 200 characters"),
  city: z
    .string()
    .trim()
    .min(1, "City is required")
    .max(200, "City must be at most 200 characters"),
  business_type: z
    .string()
    .max(200, "Business type must be at most 200 characters")
    .optional(),
  keywords: z.string().optional(),
  exclude_keywords: z.string().optional(),
  require_website: z.boolean(),
  require_contact: z.boolean(),
  require_whatsapp: z.boolean(),
  min_sources: z.coerce
    .number({ invalid_type_error: "Minimum sources must be a number" })
    .int("Must be an integer")
    .min(1, "Minimum sources must be at least 1"),
  require_official_source: z.boolean(),
  max_leads: z.coerce
    .number({ invalid_type_error: "Max leads must be a number" })
    .int("Must be an integer")
    .min(1, "Max leads must be at least 1")
    .max(100, "Max leads cannot exceed 100"),
});

type LeadFormValues = z.infer<typeof leadFormSchema>;

interface ApiResponse {
  thread_id: string;
  leads: Record<string, unknown>[];
}

interface ApiError {
  status: number;
  message: string;
}

export default function LeadGenerationPage() {
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState<ApiError | null>(null);
  const [result, setResult] = React.useState<ApiResponse | null>(null);

  const form = useForm<LeadFormValues>({
    resolver: zodResolver(leadFormSchema),
    defaultValues: {
      industry: "",
      city: "",
      business_type: "",
      keywords: "",
      exclude_keywords: "",
      require_website: true,
      require_contact: true,
      require_whatsapp: false,
      min_sources: 2,
      require_official_source: true,
      max_leads: 20,
    },
  });

  const onSubmit = async (values: LeadFormValues) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    // Parse comma-separated string into trimmed non-empty array
    const parseKeywords = (str?: string): string[] => {
      if (!str) return [];
      return str
        .split(",")
        .map((k) => k.trim())
        .filter((k) => k.length > 0);
    };

    const trimmedBusinessType = values.business_type?.trim();

    const payload = {
      industry: values.industry.trim(),
      city: values.city.trim(),
      business_type: trimmedBusinessType && trimmedBusinessType.length > 0 ? trimmedBusinessType : null,
      keywords: parseKeywords(values.keywords),
      exclude_keywords: parseKeywords(values.exclude_keywords),
      require_website: values.require_website,
      require_contact: values.require_contact,
      require_whatsapp: values.require_whatsapp,
      min_sources: Number(values.min_sources),
      require_official_source: values.require_official_source,
      max_leads: Number(values.max_leads),
    };

    try {
      const response = await fetch("/api/leads/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json().catch(() => null);

      if (!response.ok) {
        const message =
          (data && (data.message || data.error || data.detail)) ||
          "Failed to generate leads.";
        setError({
          status: response.status,
          message: typeof message === "string" ? message : JSON.stringify(message),
        });
        return;
      }

      setResult(data as ApiResponse);
    } catch (err) {
      setError({
        status: 0,
        message: err instanceof Error ? err.message : "Network failure occurred",
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Dynamically collect unique column keys across all lead objects
  const tableColumns = React.useMemo(() => {
    if (!result?.leads || !Array.isArray(result.leads)) return [];
    const keys = new Set<string>();
    for (const lead of result.leads) {
      if (lead && typeof lead === "object") {
        Object.keys(lead).forEach((key) => keys.add(key));
      }
    }
    return Array.from(keys);
  }, [result?.leads]);

  // Format cell values for plain and nested properties
  const formatCellValue = (value: unknown) => {
    if (value === null || value === undefined) {
      return <span className="text-muted-foreground">—</span>;
    }
    if (typeof value === "object") {
      return (
        <span className="font-mono text-xs break-all text-muted-foreground">
          {JSON.stringify(value)}
        </span>
      );
    }
    return String(value);
  };

  return (
    <div className="min-h-screen py-10 px-4 sm:px-6 flex flex-col items-center font-geist">
      <div className="w-full max-w-2xl space-y-8">
        {/* Lead Generation Form Card */}
        <Card className="w-full">
          <CardHeader>
            <CardTitle className="font-manrope font-normal text-2xl">
              Lead Generation
            </CardTitle>
            <CardDescription className="font-geist">
              Configure parameters to discover verified business leads.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-5">
                {/* 1. Industry */}
                <FormField
                  control={form.control}
                  name="industry"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="font-geist">Industry</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="e.g. Software, Real Estate, Healthcare"
                          className="font-geist"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {/* 2. City */}
                <FormField
                  control={form.control}
                  name="city"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="font-geist">City</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="e.g. San Francisco, London, Dubai"
                          className="font-geist"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {/* 3. Business Type */}
                <FormField
                  control={form.control}
                  name="business_type"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="font-geist">Business Type (Optional)</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="e.g. Agency, B2B SaaS, Clinic"
                          className="font-geist"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {/* 4. Keywords */}
                <FormField
                  control={form.control}
                  name="keywords"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="font-geist">Keywords</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="Comma-separated keywords, e.g. ai, automation, analytics"
                          className="font-geist"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {/* 5. Exclude Keywords */}
                <FormField
                  control={form.control}
                  name="exclude_keywords"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="font-geist">Exclude Keywords</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="Comma-separated keywords to exclude, e.g. student, intern"
                          className="font-geist"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {/* Switches Section */}
                <div className="space-y-3 pt-2">
                  <FormField
                    control={form.control}
                    name="require_website"
                    render={({ field }) => (
                      <FormItem className="flex items-center justify-between py-1">
                        <FormLabel className="font-geist cursor-pointer">
                          Require website
                        </FormLabel>
                        <FormControl>
                          <Switch
                            checked={field.value}
                            onCheckedChange={field.onChange}
                          />
                        </FormControl>
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="require_contact"
                    render={({ field }) => (
                      <FormItem className="flex items-center justify-between py-1">
                        <FormLabel className="font-geist cursor-pointer">
                          Require contact
                        </FormLabel>
                        <FormControl>
                          <Switch
                            checked={field.value}
                            onCheckedChange={field.onChange}
                          />
                        </FormControl>
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="require_whatsapp"
                    render={({ field }) => (
                      <FormItem className="flex items-center justify-between py-1">
                        <FormLabel className="font-geist cursor-pointer">
                          Require WhatsApp
                        </FormLabel>
                        <FormControl>
                          <Switch
                            checked={field.value}
                            onCheckedChange={field.onChange}
                          />
                        </FormControl>
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="require_official_source"
                    render={({ field }) => (
                      <FormItem className="flex items-center justify-between py-1">
                        <FormLabel className="font-geist cursor-pointer">
                          Require official source
                        </FormLabel>
                        <FormControl>
                          <Switch
                            checked={field.value}
                            onCheckedChange={field.onChange}
                          />
                        </FormControl>
                      </FormItem>
                    )}
                  />
                </div>

                {/* Min Sources & Max Leads */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                  <FormField
                    control={form.control}
                    name="min_sources"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="font-geist">Min Sources</FormLabel>
                        <FormControl>
                          <Input
                            type="number"
                            min={1}
                            className="font-geist"
                            {...field}
                            value={field.value ?? ""}
                            onChange={(e) =>
                              field.onChange(
                                e.target.value === "" ? "" : Number(e.target.value)
                              )
                            }
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="max_leads"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="font-geist">Max Leads</FormLabel>
                        <FormControl>
                          <Input
                            type="number"
                            min={1}
                            max={100}
                            className="font-geist"
                            {...field}
                            value={field.value ?? ""}
                            onChange={(e) =>
                              field.onChange(
                                e.target.value === "" ? "" : Number(e.target.value)
                              )
                            }
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                {/* Submit Button */}
                <Button
                  type="submit"
                  disabled={isLoading}
                  className="w-full font-geist"
                >
                  {isLoading ? "Generating leads..." : "Generate Leads"}
                </Button>
              </form>
            </Form>
          </CardContent>
        </Card>

        {/* Error Alert */}
        {error && (
          <Alert variant="destructive">
            <AlertTitle className="font-manrope font-normal">
              {error.status ? `Request Failed (Status ${error.status})` : "Network Error"}
            </AlertTitle>
            <AlertDescription className="font-geist">
              {error.message}
            </AlertDescription>
          </Alert>
        )}

        {/* Results Section */}
        {result && (
          <Card className="w-full">
            <CardHeader className="gap-2">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <CardTitle className="font-manrope font-normal text-xl">
                  Generated Results
                </CardTitle>
                {result.thread_id && (
                  <Badge variant="outline" className="font-geist">
                    {result.thread_id}
                  </Badge>
                )}
              </div>
              <CardDescription className="font-geist">
                {result.leads && result.leads.length > 0
                  ? `${result.leads.length} lead${result.leads.length === 1 ? "" : "s"} found`
                  : "0 leads found"}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {!result.leads || result.leads.length === 0 ? (
                <p className="text-sm text-muted-foreground font-geist">
                  No leads found
                </p>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      {tableColumns.map((col) => (
                        <TableHead
                          key={col}
                          className="font-manrope font-normal capitalize"
                        >
                          {col.replace(/_/g, " ")}
                        </TableHead>
                      ))}
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {result.leads.map((lead, idx) => (
                      <TableRow key={idx}>
                        {tableColumns.map((col) => (
                          <TableCell key={col} className="font-geist">
                            {formatCellValue(lead[col])}
                          </TableCell>
                        ))}
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
