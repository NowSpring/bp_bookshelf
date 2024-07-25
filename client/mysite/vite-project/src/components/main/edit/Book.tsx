import { BookType } from "../types";
import { Dialog } from "@/components/ui/dialog";
import DetailDialog from "./DetailDialog";
import { Check } from "lucide-react";
import { useEffect, useState } from "react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { MdMoreVert } from 'react-icons/md';
import SearchDialog from "../edit/search/SearchDialog";
import NoImage from "@/assets/no_image.jpg"
import "@/components/main/style.css"


type BookProps = {
  index: number;
  book: BookType;
  updateBook: (updatedBook: BookType) => void;
};

const maxTitleLength = 10;

const TextWithEllipsis = ({ text, maxLength }: { text: string; maxLength: number }) => {
  if (text.length > maxLength) {
    return `${text.substring(0, maxLength)}...`;
  }
  return text;
};

const Book: React.FC<BookProps> = ({ index, book, updateBook }) => {

  const [attentionBook, setAttentionBook] = useState<BookType>(book)

  const [isDetailDialog, setIsDetailDialog] = useState(false)
  const [isSearchDialog, setIsSearchDialog] = useState(false)

  useEffect(() => {
    updateBook(attentionBook);
  }, [attentionBook, updateBook]);

  const showDetailDialog = () =>{
    if (isDetailDialog) {
      return (
        <DetailDialog
          book={attentionBook}
        />
      )
    }
  }

  const showSearchDialog = () =>{
    if (isSearchDialog) {
      return (
        <SearchDialog
          book={attentionBook}
          setBook={setAttentionBook}
          closeDialog={() => setIsSearchDialog(false)}
        />
      )
    }
  }

  return (
    <>
    <div
      className="bookBox"
      style={{
        backgroundImage: `url(${book.image ? book.image : NoImage})`,
        backgroundSize: '140%',
        backgroundPosition: 'center 50%',
      }}
    >

      <div className="kebabMenu">
        <DropdownMenu>
          <DropdownMenuTrigger>
            <span className="kebabButton">
              <MdMoreVert size={20} />
            </span>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="dropdown-menu" align="start">
            <DropdownMenuItem onClick={() => setIsDetailDialog(true)}>
              <Check className="mr-2 h-4 w-4" />
              <span>詳細情報</span>
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => setIsSearchDialog(true)}>
              <Check className="mr-2 h-4 w-4" />
              <span>漫画登録</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      <div className="bookHeader">
        <p className="bookTitle">
          <TextWithEllipsis text={attentionBook.title || ''} maxLength={maxTitleLength} />
        </p>
      </div>

      <div className="bookFooter">
        <p className="bookOrder">
          {index + 1}位
        </p>
      </div>

    </div>

    <Dialog
    open={isDetailDialog}
    onOpenChange={setIsDetailDialog}
    >
    {showDetailDialog()}
    </Dialog>
    <Dialog
    open={isSearchDialog}
    onOpenChange={setIsSearchDialog}
    >
    {showSearchDialog()}
    </Dialog>
    </>
  );
};
export default Book
