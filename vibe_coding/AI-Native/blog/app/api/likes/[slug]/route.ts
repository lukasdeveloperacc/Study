import { NextRequest, NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';

// Path to store likes data
const LIKES_FILE = path.join(process.cwd(), 'data', 'likes.json');

// Ensure data directory and file exist
async function ensureLikesFile() {
  try {
    const dataDir = path.dirname(LIKES_FILE);
    await fs.mkdir(dataDir, { recursive: true });

    try {
      await fs.access(LIKES_FILE);
    } catch {
      // File doesn't exist, create it
      await fs.writeFile(LIKES_FILE, JSON.stringify({}));
    }
  } catch (error) {
    console.error('Error ensuring likes file:', error);
  }
}

// Read likes data
async function readLikes(): Promise<Record<string, number>> {
  await ensureLikesFile();

  try {
    const data = await fs.readFile(LIKES_FILE, 'utf-8');
    return JSON.parse(data);
  } catch {
    return {};
  }
}

// Write likes data
async function writeLikes(likes: Record<string, number>) {
  await ensureLikesFile();
  await fs.writeFile(LIKES_FILE, JSON.stringify(likes, null, 2));
}

// GET /api/likes/[slug] - Get like count for a post
export async function GET(
  request: NextRequest,
  { params }: { params: { slug: string } }
) {
  try {
    const { slug } = params;
    const likes = await readLikes();

    return NextResponse.json({
      slug,
      likes: likes[slug] || 0,
    });
  } catch (error) {
    console.error('Error getting likes:', error);
    return NextResponse.json(
      { error: 'Failed to get likes' },
      { status: 500 }
    );
  }
}

// POST /api/likes/[slug] - Update like count
export async function POST(
  request: NextRequest,
  { params }: { params: { slug: string } }
) {
  try {
    const { slug } = params;
    const body = await request.json();
    const { action } = body;

    const likes = await readLikes();
    const currentLikes = likes[slug] || 0;

    if (action === 'like') {
      likes[slug] = currentLikes + 1;
    } else if (action === 'unlike') {
      likes[slug] = Math.max(0, currentLikes - 1);
    } else {
      return NextResponse.json(
        { error: 'Invalid action' },
        { status: 400 }
      );
    }

    await writeLikes(likes);

    return NextResponse.json({
      slug,
      likes: likes[slug],
    });
  } catch (error) {
    console.error('Error updating likes:', error);
    return NextResponse.json(
      { error: 'Failed to update likes' },
      { status: 500 }
    );
  }
}
