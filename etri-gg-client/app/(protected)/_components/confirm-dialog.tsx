import {
  AlertDialog, AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { Button } from "@/components/ui/button";
import { useState } from "react";

interface ConfirmDialogProps {
  children?: React.ReactNode
  title?: string
  description?: string
  onProceed: () => void
}

export function ConfirmDialog({ children, title, description, onProceed }: ConfirmDialogProps) {
  const [open, setOpen] = useState(false);

  const handleProceed =() => {
    setOpen(false);
    onProceed();
  }

  return (
    <AlertDialog open={open} onOpenChange={setOpen}>
      <AlertDialogTrigger asChild>
        {children}
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>{title}</AlertDialogTitle>
          <AlertDialogDescription>
            {description}
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <Button variant="secondary" onClick={() => setOpen(false)}>
            Cancel
          </Button>
          <Button
            onClick={handleProceed}
            variant="destructive"
          >
            Proceed
          </Button>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}
