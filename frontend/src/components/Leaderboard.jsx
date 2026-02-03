import { useEffect, useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "./ui/card";
import { Badge } from "./ui/badge";
import { apiGet, apiPost } from "../api/client";

export default function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const data = await apiPost("/leaderboard/");
        setLeaderboard(data);
      } catch (err) {
        setError("Failed to load leaderboard");
      } finally {
        setIsLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  const getRankBadgeColor = (rank) => {
    switch (rank) {
      case 1:
        return "bg-yellow-500 text-white";
      case 2:
        return "bg-gray-400 text-white";
      case 3:
        return "bg-orange-600 text-white";
      default:
        return "bg-muted text-foreground";
    }
  };

  const getRankEmoji = (rank) => {
    switch (rank) {
      case 1:
        return "🥇";
      case 2:
        return "🥈";
      case 3:
        return "🥉";
      default:
        return `#${rank}`;
    }
  };

  return (
    <Card className="sticky top-4 h-fit">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg">Leaderboard</CardTitle>
        <CardDescription>
          Top contributors in last 24 hours
        </CardDescription>
      </CardHeader>

      <CardContent>
        {isLoading ? (
          <div className="text-sm text-muted-foreground">Loading...</div>
        ) : error ? (
          <div className="text-sm text-destructive">{error}</div>
        ) : leaderboard?.leaders?.length > 0 ? (
          <div className="space-y-3">
            {leaderboard.leaders.map((entry) => (
              <div
                key={entry.rank}
                className="flex items-center justify-between gap-3"
              >
                <div className="flex items-center gap-2 flex-1 min-w-0">
                  <Badge
                    className={`${getRankBadgeColor(
                      entry.rank
                    )} shrink-0`}
                  >
                    {getRankEmoji(entry.rank)}
                  </Badge>

                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium truncate">
                      {entry.username}
                    </p>
                  </div>
                </div>

                <span className="text-sm font-semibold text-muted-foreground shrink-0">
                  {entry.karma}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-sm text-muted-foreground">
            No data available
          </div>
        )}
      </CardContent>
    </Card>
  );
}
